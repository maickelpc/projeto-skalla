from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.urls import RotasApi
from django.conf import settings
from django.conf.urls.static import static

# from core import views
from web import views as webview

urlpatterns = [
    path('', webview.criaEscala),
    path('criaescala/', webview.criaEscala),
    path('minhaescala/', webview.minhaEscala),
    path('imprimirminhaescala/', webview.imprimirMinhaEscala),
    path('gestaoescalas/', webview.gestaoEscala),
    path('solicitacoes/', webview.solicitacoes),
    path('escalas/', webview.escalas),
    path('imprimirescalas/', webview.imprimirEscalas),
    path('imprimirescala/', webview.imprimirEscala),
    path('api/', include(RotasApi.rotasApi.urls)),
    path('admin/', admin.site.urls),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
