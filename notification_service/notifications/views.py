from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Client, Dispatch
from .serializers import ClientSerializer, DispatchSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = (IsAuthenticated, )

class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.all()
    serializer_class = DispatchSerializer
    permission_classes = (IsAuthenticated, )
