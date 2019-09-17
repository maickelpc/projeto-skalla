from rest_framework import serializers
from .models import Endereco, Cidade

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ('__all__')


class EnderecoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ('__all__')