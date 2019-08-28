from django import forms

from pessoa.models import Usuario


class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Usuario