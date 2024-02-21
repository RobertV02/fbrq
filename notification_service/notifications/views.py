from django.contrib.auth.hashers import make_password
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Client, Dispatch
from .serializers import ClientSerializer, DispatchSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
#    permission_classes = (IsAuthenticated, )

class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
#    permission_classes = (IsAuthenticated, )