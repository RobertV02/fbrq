from django.contrib import admin
from django.contrib import admin
from .models import Dispatch, Client, Message

# Register your models here.
admin.site.register(Dispatch)
admin.site.register(Client)
admin.site.register(Message)
