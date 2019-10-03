
from django.shortcuts import render
import datetime
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
    serializer_class = EscalaSimplificadoSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend)
    search_fields = ()
    filter_fields = ['turnoPonto','perfil','status']
    ordering_fields = '__all__'


class EscalaColaboradorViewSet(viewsets.ModelViewSet):
    queryset = EscalaColaborador.objects.order_by('dataInicio').all()
    serializer_class = EscalaColaboradorSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend)
    search_fields = ()
    filter_fields = ['escala','colaborador']
    ordering_fields = '__all__'
    parser_classes = [JSONParser]

    @action(methods=['post'], detail=False)
    def confirma(self, request):

        escala = request.data

        print (escala['id'])
        escalaColaborador = EscalaColaborador.objects.filter(id=int(escala['id'])).get()
        escalaColaborador.status = 1;
        escalaColaborador.dataConfirmacao = datetime.datetime.now();
        escalaColaborador.save()

        return Response({'Ok:'})


    @action(methods=['post'], detail=False)
    def registrasolicitacao(self, request):
        escala = request.data

        print(escala['id'])
        escalaColaborador = EscalaColaborador.objects.filter(id=int(escala['id'])).get()
        escalaColaborador.statusSolicitacao = 1;
        escalaColaborador.dataSolicitacaoAlteracao = datetime.datetime.now();
        escalaColaborador.solicitacaoAlteracao = escala['solicitacaoAlteracao'];

        escalaColaborador.save()

        return Response({'Ok:'})
