from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from notifications.views import *


routerC = routers.SimpleRouter()
routerC.register(r'client', ClientViewSet)

routerD = routers.SimpleRouter()
routerD.register(r'dispatch', DispatchViewSet)


api = [
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(routerC.urls)),
    path('api/v1/', include(routerD.urls)),
    path('api/v1/', include(api)),
]
