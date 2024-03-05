from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from notifications.views import *
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

routerC = routers.SimpleRouter()
routerC.register(r'client', ClientViewSet)

routerD = routers.SimpleRouter()
routerD.register(r'dispatch', DispatchViewSet)

api = [
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]

# Настроим Swagger UI
schema_view = get_schema_view(
   openapi.Info(
      title="Notification Service API",
      default_version='v1',
      description="API для управления рассылками и получения статистики по отправленным сообщениям",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="rob.pap@mail.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(routerC.urls)),
    path('api/v1/', include(routerD.urls)),
    path('api/v1/', include(api)),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
