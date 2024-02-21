from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from notifications.views import *


router = routers.SimpleRouter()
router.register(r'client', ClientViewSet)

api = [

]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]
