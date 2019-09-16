from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.urls import rotasApi

from core import views

urlpatterns = [
    path('', views.hello),
    path('api/', include(rotasApi.rotas.urls)),
    path('admin/', admin.site.urls),
]
