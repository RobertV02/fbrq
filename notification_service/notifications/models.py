from django.db import models


class Mailing(models.Model):
    id = models.AutoField(primary_key=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    message = models.TextField()
    filter_clients = models.CharField()
    f_datetime = models.DateTimeField()
    def __str__(self):
        return f"Mailing {self.id}"
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=12)
    mobile_operator_code = models.CharField(max_length=10)
    tag = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50)

    def __str__(self):
        return f"Client {self.id}"

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    status = models.CharField(max_length=50)
    dispatch = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"Message {self.id}"