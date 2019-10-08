from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.urls import RotasApi

from core import views
from web import views as webview

urlpatterns = [
    # path('', views.hello),
    path('', views.index),
    path('minhaescala/', webview.minhaEscala),
    path('gestaoescalas/', webview.gestaoEscala),
    path('api/', include(RotasApi.rotasApi.urls)),
    path('admin/', admin.site.urls),
]
