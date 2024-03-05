from rest_framework import serializers
from .models import Client, Dispatch
from django.contrib.auth.models import User
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
class DispatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dispatch
        fields = "__all__"