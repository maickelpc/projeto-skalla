from django.utils import timezone
import datetime
import pytz
from django.db import transaction
from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from .serializers import ClienteCompletoSerializer, ClienteSimpleSerializer, PontoAlocacaoSerializer, \
    PerfilJornadaSerializer,  Turno_PontoAlocacaoSerializer, EscalaSimplificadoSerializer, EscalaSerializer,\
    EscalaColaboradorSerializer, EscalaColaboradorSimplificadoSerializer
from .models import Cliente, PontoAlocacao, PerfilJornada, Turno_PontoAlocacao, EscalaColaborador, Escala
from empresa.models import Colaborador
from core.models import Configuracao


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

    @action(methods=['get'], detail=True)
    def cancelarescala(self, request, pk=None):

        # rq = request.data
        # escala = Escala.objects.get(id=int(rq['id']))
        escala = Escala.objects.get(id=pk)
        if escala.status == 1:
            return Response('Esta escala já foi cancelada em: ' + escala.dataCancelamento.strftime("%d/%m/%Y %H:%M:%S"), 400)

        colaborador = Colaborador.objects.get(pk=request.user.id)
        configuracoes = Configuracao.objects.first()
        agora = pytz.UTC.localize(datetime.datetime.now() + datetime.timedelta(hours=1))
        dias = colaborador.empresa.diasAntecedenciaSolicitacao
        datalimite = escala.dataInicio + datetime.timedelta(days=-dias)

        #Se estourou o tempo limite, e o usuário não é gestor/admin
        if agora > datalimite and not colaborador.groups.filter(pk=configuracoes.grupoGestor.id).exists():
            return Response('Somente Administradores podem cancelar esta escala após: ' + datalimite.strftime("%d/%m/%Y %H:%M:%S"), 400)

        # Criar metodo para cancelar todas as escalaColaborador envolvidas.
        try:
            with transaction.atomic():
                timezone.activate('America/Sao_Paulo')
                agora = timezone.now()

                escala.status = 1
                escala.dataCancelamento = agora
                escala.save()

                escalados = EscalaColaborador.objects.filter(escala=escala).all()
                for e in escalados:
                    e.dataCancelamento = agora
                    e.status = 3
                    e.save()

                serializer = EscalaSerializer(escala)
                return Response(serializer.data)
        except:
            return Response('Erro ao Cancelar a escala', 400)



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
            dataInicial = datetime.datetime.strptime(dataInicial, '%Y-%m-%d')
            queryset = queryset.filter(dataInicio__gte=dataInicial)


        if dataFinal:
            dataFinal = datetime.datetime.strptime(dataFinal, '%Y-%m-%d') + datetime.timedelta(days=1)
            queryset = queryset.filter(dataInicio__lt=dataFinal)


        if status and int(status) > -1:
            # Status: -1: Todos | 0: Pendente | 1: Confirmado | 4: Executado | 2: Cancelado | 3 - Rejeitado
            status = int(status)

            hoje = datetime.datetime.now()
            if status == 4:
                queryset = queryset.filter(dataInicio__lt=hoje).exclude(status=2).exclude(status=3)
            else:
                queryset = queryset.filter(dataInicio__gt=hoje).filter(status=status)


        return queryset

    @action(methods=['get'], detail=True)
    def cancelar(self, request, pk=None):
        escalaColaborador = EscalaColaborador.objects.get(id=pk)

        if escalaColaborador.escala.status == 1:
            return Response('Esta escala já foi cancelada em: ' + escalaColaborador.escala.dataCancelamento.strftime("%d/%m/%Y %H:%M:%S"), 400)

        if escalaColaborador.status == 3:
            return Response('Esta escala já foi cancelada em: ' + escalaColaborador.dataCancelamento.strftime("%d/%m/%Y %H:%M:%S"), 400)
        print(request.user.id)
        colaborador = Colaborador.objects.get(pk=request.user.id)
        configuracoes = Configuracao.objects.first()
        agora = pytz.UTC.localize(datetime.datetime.now() + datetime.timedelta(hours=1))
        dias = colaborador.empresa.diasAntecedenciaSolicitacao
        datalimite = escalaColaborador.escala.dataInicio + datetime.timedelta(days=-dias)
        # Se estourou o tempo limite, e o usuário não é gestor/admin
        if agora > datalimite and not colaborador.groups.filter(pk=configuracoes.grupoGestor.id).exists():
            return Response('Somente Administradores podem cancelar esta escala após: ' + datalimite.strftime("%d/%m/%Y %H:%M:%S"), 400)

        # Criar metodo para cancelar todas as escalaColaborador envolvidas.
        try:
            with transaction.atomic():
                timezone.activate('America/Sao_Paulo')
                agora = timezone.now()
                escalaColaborador.dataCancelamento = agora
                escalaColaborador.status = 3
                escalaColaborador.save()
                serializer = EscalaColaboradorSimplificadoSerializer(escalaColaborador)

                return Response(serializer.data)
        except:
            return Response('Erro ao Cancelar a escala', 400)

    @action(methods=['get'], detail=False)
    def ultimas(self, request):

        data = self.request.query_params.get('data', None)
        colaborador = int(self.request.query_params.get('colaborador', None))

        if(data):
            data = datetime.datetime.strptime(data, '%Y-%m-%d')
        else:
            data = datetime.datetime.now()

        escalasAnteriores = EscalaColaborador.objects.filter(colaborador=colaborador, status__in=[0,1], dataInicio__lte=data).order_by('-dataInicio').all()[:3]
        escalasFuturas = EscalaColaborador.objects.filter(colaborador=colaborador, status__in=[0,1], dataInicio__gte=data).order_by('dataInicio').all()[:3]

        escalas = escalasAnteriores | escalasFuturas;

        serializer = EscalaColaboradorSerializer(escalas, many=True)

        return Response(serializer.data)

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
        colaborador = Colaborador.objects.get(pk=request.user.id)
        configuracoes = Configuracao.objects.first()
        #Valida se a escala ainda está em prazo de receber solicitação
        if agora > datalimite and not colaborador.groups.filter(pk=configuracoes.grupoGestor.id).exists():
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
        escalaColaborador.dataRetornoSolicitacaoAlteracao = datetime.datetime.now()
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

