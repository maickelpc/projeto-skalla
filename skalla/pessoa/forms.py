from django import forms

from pessoa.models import Usuario


class UsuarioForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    class Meta:
        model = Usuario
        fields = '__all__'

