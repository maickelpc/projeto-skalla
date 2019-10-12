from rest_framework import serializers
from .models import  Cidade

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ('__all__')
