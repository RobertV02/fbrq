from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from .models import Client
from .serializers import ClientSerializer



class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


