from django import forms
from empresa.models import Empresa

class Formulario(forms.ModelForm):
    campoqua = forms.CharField(max_length=100, required=True, label="Nome")

    class Meta:
        model = Empresa
        fields = '__all__'
