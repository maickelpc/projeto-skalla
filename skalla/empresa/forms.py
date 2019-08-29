from django import  forms

from .models import Empresa

class EmpresaForm(forms.ModelForm):

    RazaoSocial = forms.CharField(max_length=50, initial = 'model.pessoa.nome')

    class Meta:
        model = Empresa
        fields = ('RazaoSocial','nomeFantasia','logo')
        # fields = ('__all__')

    def save(self, commit=True):

        m = super(EmpresaForm, self).save(commit=False)
        # do custom stuff
        if commit:
            m.save()

        return m

