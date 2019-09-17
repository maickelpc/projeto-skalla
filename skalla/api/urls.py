from rest_framework import routers
from cliente.views import ClienteViewSet, PerfilJornadaViewSet
from empresa.views import ColaboradorViewSet

class RotasApi():
    rotasApi = routers.DefaultRouter()
    rotasApi.register('cliente', ClienteViewSet, 'Cliente')
    rotasApi.register('perfil-jornada', PerfilJornadaViewSet, 'PerfilJornada')
    rotasApi.register('colaborador', ColaboradorViewSet, 'Colaborador')