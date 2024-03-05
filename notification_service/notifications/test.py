import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from celery import Celery, shared_task, group
from dotenv import load_dotenv
from django.utils import timezone
from notifications.models import Dispatch, Client, Message
import requests
import logging
from datetime import datetime


app = Celery('tasks', broker='redis://localhost:6379/0')
load_dotenv()
success_msg = 0
# Конфигурируем логгер

def log_message_dispatch_info(dispatch_id, sent_time, client_id, message_id):
    log_message = f"Dispatch ID: {dispatch_id}, Message ID: {message_id}, Sent Time: {sent_time}, Client ID: {client_id}"
    with open('message_logs.log', 'a', encoding='utf-8') as file:
        file.write(f"{datetime.now()} - INFO - {log_message}\n")

def log_error(message_id, error_message):
    log_message = f"Error occurred while sending message with ID {message_id}: {error_message}"
    with open('message_logs.log', 'a', encoding='utf-8') as file:
        file.write(f"{datetime.now()} - ERROR - {log_message}\n")

def clear_data():
    global success_msg
    success_msg = 0
@app.task
def send_email(result = None):
    # Email sending logic
    sender_email = os.environ.get("EMAIL_SENDER")
    password = os.environ.get("EMAIL_PASSWORD")

    receiver_email = "example@mail.ru"  # Замените на нужный адрес


    message = MIMEMultipart("alternative")
    message["Subject"] = "Celery Task Result"
    message["From"] = sender_email
    message["To"] = receiver_email

    text = f"Result of my_task: "
    html = f"<p>Result of my_task: {success_msg} Выполненных рассылок за сегодня</p>"

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL("smtp.yandex.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    clear_data()


@shared_task()
def send_message_to_external_api(message_id):
    global success_msg
    message = Message.objects.get(id=message_id)
    message.status = "102"
    message.save()
    # Подготавливаем данные для отправки на внешний API
    data = {
        "id": message.id,
        "phone": message.client.phone_number,
        "text": message.dispatch.message
    }

    # URL внешнего API
    url = "https://probe.fbrq.cloud/v1/send/{}".format(message.id)
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzkzNDg3ODYsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9GcmVlbGVhdmVlZSJ9.GLMLbbCX9C-3FlwItD8sLWrafNZTmg9Zu6cE9IPDJcA"
    }

    try:
        # Отправляем POST запрос на внешний API с заголовком авторизации
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Проверяем успешность запроса
        # Получаем код состояния HTTP ответа
        status_code = response.status_code

        # Обновляем статус сообщения в базе данных
        message.status = status_code
        message.save()
        current_time = datetime.now()
        log_message_dispatch_info(message.dispatch.id, current_time, message.client.id, message_id)
        success_msg += 1
        print("Сообщение успешно отправлено. Код состояния: " + str(status_code))
    except requests.RequestException as e:
        message.status = "400"
        message.save()
        print("Ошибка при отправке сообщения:", e)
        log_error(message_id, e)


@app.task
def my_task():
    dispatches = Dispatch.objects.all()
    for d in dispatches:
        if d.start_datetime <= timezone.now() <= d.end_datetime:
            print("Рассылка: " + str(d.id))
            send_tasks = []

            if d.tag_filter != "" and d.code_filter != "":
                tag_obj = Client.objects.filter(tag = d.tag_filter, mobile_operator_code = d.code_filter)
            elif d.tag_filter != "":
                tag_obj = Client.objects.filter(tag=d.tag_filter)
            elif d.code_filter != "":
                tag_obj = Client.objects.filter(mobile_operator_code=d.code_filter)
            for t in tag_obj:
                if t.local_start_datetime is not None and t.local_end_datetime is not None:
                    if not t.local_start_datetime <= timezone.now() <= t.local_end_datetime:
                        print("у него время не соответствует " + str(t.id))
                        continue
                existmsg = Message.objects.filter(start_datetime = d.start_datetime, client = t, dispatch = d)
                if existmsg:
                    for msg in existmsg:
                        if msg.status == "0" or msg.status == "400":
                            send_tasks.append(send_message_to_external_api.s(msg.id))
                else:
                    msg = Message.objects.create(
                        start_datetime = d.start_datetime,
                        end_datetime = d.end_datetime,
                        status = "0",
                        dispatch = d,
                        client = t
                    )
                    print("Отправляется рассылка клиенту: " + str(t.id))
                    send_tasks.append(send_message_to_external_api.s(msg.id))

            print("Рассылка для ", send_tasks)
            group(*send_tasks)()
    return "Рассылка успешно завершена"

