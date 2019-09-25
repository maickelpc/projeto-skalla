from django.shortcuts import render
from .models import Cliente, PontoAlocacao, Turno, PerfilJornada, Turno_PontoAlocacao
from empresa.models import Colaborador

from core.serializers import EnderecoSimpleSerializer
from rest_framework import serializers

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ('__all__')

class PontoAlocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PontoAlocacao
        fields = ('__all__')

class Turno_PontoAlocacaoSerializer(serializers.ModelSerializer):
    turno = TurnoSerializer()
    class Meta:
        model = Turno_PontoAlocacao
        fields = ('__all__')

class ClienteSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id','nomeFantasia')

class ClienteCompletoSerializer(serializers.ModelSerializer):
    pontosAlocacao = PontoAlocacaoSerializer( many=True, read_only=True, source='cliente_ponto')
    endereco = EnderecoSimpleSerializer()
    class Meta:
        model = Cliente
        fields = ['id','nomeFantasia','CNPJ','IE','IM','logo','endereco','telefone','contatoEscala','contatoEscalaFone', 'pontosAlocacao']


class PerfilJornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilJornada
        fields = ('__all__')