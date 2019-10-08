from django.shortcuts import render
from .models import Cliente, PontoAlocacao, Turno, PerfilJornada, Turno_PontoAlocacao, Escala, EscalaColaborador
from empresa.models import Colaborador
from empresa.serializers import ColaboradorSerializer

from rest_framework import serializers

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ('__all__')

class ClienteSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id','nomeFantasia')



class PontoAlocacaoSerializer(serializers.ModelSerializer):
    cliente = ClienteSimpleSerializer()
    class Meta:
        model = PontoAlocacao
        fields = ('__all__')



class Turno_PontoAlocacaoSerializer(serializers.ModelSerializer):
    turno = TurnoSerializer()
    pontoAlocacao = PontoAlocacaoSerializer()
    class Meta:
        model = Turno_PontoAlocacao
        fields = ('__all__')



class ClienteCompletoSerializer(serializers.ModelSerializer):
    pontosAlocacao = PontoAlocacaoSerializer( many=True, read_only=True, source='cliente_ponto')
    class Meta:
        model = Cliente
        # fields = ['id','nomeFantasia','CNPJ','IE','IM','logo','endereco','telefone','contatoEscala','contatoEscalaFone', 'pontosAlocacao']
        fields = ('__all__')


class PerfilJornadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilJornada
        fields = ('__all__')


class EscalaSimplificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escala
        fields = ('__all__')

class EscalaSerializer(serializers.ModelSerializer):
    turnoPonto = Turno_PontoAlocacaoSerializer()
    perfil = PerfilJornadaSerializer
    class Meta:
        model = Escala
        fields = ('__all__')



class EscalaColaboradorSimplificadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscalaColaborador
        fields = ('__all__')


class EscalaColaboradorSerializer(serializers.ModelSerializer):
    escala = EscalaSerializer()
    colaborador = ColaboradorSerializer
    class Meta:
        model = EscalaColaborador
        fields = ('__all__')