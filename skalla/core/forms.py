from django import forms
from empresa.models import Empresa
from cliente.models import Cliente, Turno, PontoAlocacao

class Formulario(forms.ModelForm):
    campoqua = forms.CharField(max_length=100, required=True, label="Nome")

    class Meta:
        model = Empresa
        fields = '__all__'


class FormInicialEscala(forms.Form):
    cliente = forms.ChoiceField(label='Cliente:', choices=[('0', '-- Selecione --')] +
                                        [(cliente.id, cliente.nome) for cliente in Cliente.objects.all()])
    turno = forms.ChoiceField(label='Turno', choices=[('0', '-- Selecione --')] +
                                        [(turno.id, turno.descricao) for turno in Turno.objects.all()])
    ponto = forms.ChoiceField(choices=[('0', '-- Selecione --')] +
                                        [(ponto.id, ponto.nome) for ponto in PontoAlocacao.objects.all()])