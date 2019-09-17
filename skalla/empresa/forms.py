from django import forms
from .models import Colaborador


class ColaboradorForm(forms.ModelForm):

    class Meta:
        model = Colaborador
        exclude = ['password']
        fields = ['username', 'first_name','last_name', 'email','dataNascimento','empresa','departamento','telefone','celular','contato',
                  'contatoFone','limiteHorasSemana','limiteHorasMes','PIS','dataAdmissao']

