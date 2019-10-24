from django.core import serializers
from django.core.serializers import serialize
from django.shortcuts import render
import datetime
from datetime import timedelta
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.filters import SearchFilter


from .serializers import ColaboradorSerializer
from .models import Colaborador, PeriodoInativo
from cliente.models import EscalaColaborador

class ColaboradorViewSet(viewsets.ModelViewSet):
    # queryset = Colaborador.objects.all()
    # queryset = Colaborador.objects.filter(dataAdmissao__lte=datetime.datetime.now().today()) #LT < que
    # queryset = Colaborador.objects.filter(dataAdmissao__gte=datetime.datetime.now().today()) #GT > que
    queryset = Colaborador.objects.exclude(colaborador_periodo__dataInicio__lte=datetime.datetime.now().today(),colaborador_periodo__dataFim__gte=datetime.datetime.now().today())
    serializer_class = ColaboradorSerializer
    filter_backends = (SearchFilter,)

    search_fields = ('id','email','username','first_name','last_name')

    def get_queryset(self):
        data = self.request.query_params.get('data', None)

        queryset = Colaborador.objects.order_by('first_name').all()
        if data:
            dia = datetime.datetime.strptime(data, '%Y-%m-%d') + timedelta(hours=0)
            diaSeguinte = datetime.datetime.strptime(data, '%Y-%m-%d') + timedelta(days=1)

            # Pensar melhor nesta logica, para trazer apenas os colaboradores que não tem escala para a DATA em questão
            queryset = Colaborador.objects.exclude(colaborador_periodo__dataInicio__lte=data,colaborador_periodo__dataFim__gte=data)

            # .exclude(colaborador_escala__dataInicio__gte=dia, colaborador_escala__dataInicio__lt=diaSeguinte,colaborador_escala__status__in=[0, 1])

        return queryset