from rest_framework import routers
from cliente.views import ClienteViewSet, PerfilJornadaViewSet, PontoAlocacaoViewSet, TurnoPontoAlocacaoViewSet, EscalaViewSet, EscalaColaboradorViewSet
from empresa.views import ColaboradorViewSet

class RotasApi():
    rotasApi = routers.DefaultRouter()
    rotasApi.register('colaborador', ColaboradorViewSet, 'Colaborador')
    rotasApi.register('escala', EscalaViewSet, 'Escala')
    rotasApi.register('escala-colaborador', EscalaColaboradorViewSet, 'EscalaColaborador')


    rotasApi.register('cliente', ClienteViewSet, 'Cliente')
    rotasApi.register('perfil-jornada', PerfilJornadaViewSet, 'PerfilJornada')
    rotasApi.register('ponto-alocacao', PontoAlocacaoViewSet, 'PontoAlocacao')
    rotasApi.register('turno-ponto', TurnoPontoAlocacaoViewSet, 'TurnoPontoAlocacao')