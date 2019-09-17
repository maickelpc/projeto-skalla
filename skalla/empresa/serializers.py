from .models import Colaborador, Area, Departamento
from rest_framework import serializers

class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = ('__all__')

class DepartamentoSerializer(serializers.ModelSerializer):
    area = AreaSerializer()
    class Meta:
        model = Departamento
        fields = ('__all__')

class ColaboradorSerializer(serializers.ModelSerializer):
    departamento = DepartamentoSerializer()

    class Meta:
        model = Colaborador
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "telefone",
            "celular",
            "contato",
            "contatoFone",
            "limiteHorasMes",
            "limiteHorasSemana",
            "departamento",
            ]

