
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


class EscalaColaboradorViewSet(viewsets.ModelViewSet):
    queryset = EscalaColaborador.objects.order_by('dataInicio').all()
    serializer_class = EscalaColaboradorSerializer
    filter_backends = (SearchFilter,DjangoFilterBackend)
    search_fields = ()
    filter_fields = ['id','escala','colaborador']
    ordering_fields = '__all__'
    parser_classes = [JSONParser]

    def get_queryset(self):

        dataInicial = self.request.query_params.get('dataInicial', None)
        dataFinal  = self.request.query_params.get('dataFinal', None)

        status = self.request.query_params.get('status', None)

        queryset = EscalaColaborador.objects.order_by('dataInicio').all()
        if dataInicial:
            print(dataInicial)
            dataInicial = datetime.datetime.strptime(dataInicial, '%Y-%m-%d')
            queryset = queryset.filter(dataInicio__gte=dataInicial)


        if dataFinal:
            print(dataFinal)
            dataFinal = datetime.datetime.strptime(dataFinal, '%Y-%m-%d') + datetime.timedelta(days=1)
            queryset = queryset.filter(dataInicio__lt=dataFinal)


        if status and int(status) > -1:
            # Status: -1: Todos | 0: Pendente | 1: Confirmado | 4: Executado | 2: Cancelado | 3 - Rejeitado

            status = int(status)
            print(status);
            hoje = datetime.datetime.now()
            if status == 4:
                print("DataInicio ANTERIOR á hoje")
                queryset = queryset.filter(dataInicio__lt=hoje).exclude(status=2).exclude(status=3)
            else:
                print("DataInicio POSTERIOR á hoje")
                queryset = queryset.filter(dataInicio__gt=hoje).filter(status=status)



        return queryset

    @action(methods=['post'], detail=False)
    def confirma(self, request):
        escala = request.data
        escalaColaborador = EscalaColaborador.objects.filter(id=int(escala['id'])).get()
        escalaColaborador.status = 1;
        escalaColaborador.dataConfirmacao = datetime.datetime.now();
        escalaColaborador.save()
        return Response({'Ok:'})


    @action(methods=['post'], detail=False)
    def registrasolicitacao(self, request):
        escala = request.data
        escalaColaborador = EscalaColaborador.objects.filter(id=int(escala['id'])).get()
        dias = escalaColaborador.colaborador.empresa.diasAntecedenciaSolicitacao
        datalimite = escalaColaborador.dataInicio + datetime.timedelta(days=-dias)
        agora = pytz.UTC.localize(datetime.datetime.now() + datetime.timedelta(hours=1))

        #Valida se a escala ainda está em prazo de receber solicitação
        if agora > datalimite:
            return Response('Esta escala não pode receber solicitações, pois ultrapassou o tempo limite: ' + datalimite.strftime("%d/%m/%Y %H:%M:%S"), 400)


        escalaColaborador.statusSolicitacao = 1;
        escalaColaborador.dataSolicitacaoAlteracao = datetime.datetime.now();
        escalaColaborador.solicitacaoAlteracao = escala['solicitacaoAlteracao'];

        escalaColaborador.save()

        return Response({'Ok:'})

    @action(methods=['post'], detail=False)
    def retornosolicitacao(self, request):
        escala = request.data

        print(escala['id'])
        escalaColaborador = EscalaColaborador.objects.filter(id=int(escala['id'])).get()

        escalaColaborador.statusSolicitacao = escala['statusSolicitacao'];
        escalaColaborador.dataRetornoSolicitacaoAlteracao = datetime.datetime.now();
        escalaColaborador.retornoSolicitacao = escala['retornoSolicitacao'];

        escalaColaborador.save()

        return Response({'Ok:'})


    @action(methods=['get'], detail=False)
    def solicitacoes(self, request):

        dataInicial = self.request.query_params.get('dataInicial', None)
        dataFinal = self.request.query_params.get('dataFinal', None)
        id = self.request.query_params.get('id', None)
        colaborador = self.request.query_params.get('colaborador', None)
        statusSolicitacao = self.request.query_params.get('statusSolicitacao', None)


        queryset = EscalaColaborador.objects.order_by('dataInicio').all()

        if id:
            id = int(id)
            queryset = queryset.filter(pk=id)

        if colaborador:
            colaborador = int(colaborador)
            queryset = queryset.filter(colaborador=colaborador)


        if statusSolicitacao:
            statusSolicitacao = int(statusSolicitacao)
            queryset = queryset.filter(statusSolicitacao=statusSolicitacao)

        if dataInicial:
            dataInicial = datetime.datetime.strptime(dataInicial, '%Y-%m-%d')
        else:
            dataInicial = datetime.datetime.now() + datetime.timedelta(days=-7)
        queryset = queryset.filter(dataSolicitacaoAlteracao__gte=dataInicial)

        if dataFinal:
            dataFinal = datetime.datetime.strptime(dataFinal, '%Y-%m-%d') + datetime.timedelta(days=1)
        else:
            dataFinal = datetime.datetime.now() + datetime.timedelta(days=1)
        queryset = queryset.filter(dataSolicitacaoAlteracao__lt=dataFinal)

        dados = queryset.all()
        serializer = EscalaColaboradorSerializer(dados, many=True)

        return Response(serializer.data)

