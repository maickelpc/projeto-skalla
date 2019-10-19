
from django.shortcuts import render
import datetime
import pytz
from datetime import timedelta
from django.shortcuts import render
import json
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.core.files import temp as tempfile
from django.core.files.uploadedfile import UploadedFile

from .serializers import ClienteCompletoSerializer, \
    ClienteSimpleSerializer, \
    PontoAlocacaoSerializer, \
    PerfilJornadaSerializer, \
    Turno_PontoAlocacaoSerializer, \
    EscalaSimplificadoSerializer, EscalaSerializer, \
    EscalaColaboradorSerializer, EscalaColaboradorSimplificadoSerializer
from .models import Cliente, PontoAlocacao, PerfilJornada, Turno_PontoAlocacao, EscalaColaborador, Escala


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteCompletoSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend,)
    search_fields = ('id','nomeFantasia','CNPJ','IE','IM','telefone','contatoEscala','contatoEscalaFone')
    filter_fields = ['id']


class PontoAlocacaoViewSet(viewsets.ModelViewSet):
    queryset = PontoAlocacao.objects.all()
    serializer_class = PontoAlocacaoSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend)
    search_fields = ('id','cliente__nome','descricao')
    filter_fields = ['id','cliente']


class TurnoPontoAlocacaoViewSet(viewsets.ModelViewSet):
    queryset = Turno_PontoAlocacao.objects.all()
    serializer_class = Turno_PontoAlocacaoSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend,)
    search_fields = ('id')
    filter_fields = ['id','pontoAlocacao','turno']



class PerfilJornadaViewSet(viewsets.ModelViewSet):
    queryset = PerfilJornada.objects.all()
    serializer_class = PerfilJornadaSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('tipo','descricao')


class EscalaViewSet(viewsets.ModelViewSet):
    queryset = Escala.objects.all()
    serializer_class = EscalaSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend)
    search_fields = ()
    filter_fields = ['id','perfil','status']
    ordering_fields = '__all__'

    def get_queryset(self):

        dataInicial = self.request.query_params.get('dataInicial', None)
        dataFinal  = self.request.query_params.get('dataFinal', None)
        cliente  = self.request.query_params.get('cliente', None)
        pontoAlocacao  = self.request.query_params.get('pontoalocacao', None)
        # colaborador  = self.request.query_params.get('colaborador', None)


        queryset = Escala.objects.order_by('dataInicio').all()

        if dataInicial:
            dataInicial = datetime.datetime.strptime(dataInicial, '%Y-%m-%d')
            queryset = queryset.filter(dataInicio__gte=dataInicial)

        if dataFinal:
            dataFinal = datetime.datetime.strptime(dataFinal, '%Y-%m-%d') + datetime.timedelta(days=1)
            queryset = queryset.filter(dataInicio__lt=dataFinal)

        if cliente:
            cliente = int(cliente)
            queryset = queryset.filter(turnoPonto__pontoAlocacao__cliente=cliente)

        if pontoAlocacao:
            pontoAlocacao = int(pontoAlocacao)
            queryset = queryset.filter(turnoPonto__pontoAlocacao=pontoAlocacao)
        return queryset

