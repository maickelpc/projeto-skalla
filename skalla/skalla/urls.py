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
    path('', views.index),
    path('criaescala/', webview.criaEscala),
    path('minhaescala/', webview.minhaEscala),
    path('imprimirminhaescala/', webview.imprimirMinhaEscala),
    path('gestaoescalas/', webview.gestaoEscala),
    path('solicitacoes/', webview.solicitacoes),
    path('escalas/', webview.escalas),
    path('api/', include(RotasApi.rotasApi.urls)),
    path('admin/', admin.site.urls),
]
