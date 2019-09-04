from django import  forms
from .models import Empresa









# class EmpresaForm(forms.ModelForm):
#
#     # pessoa__nome = forms.CharField(max_length=50, label="Razão Social")
#     # pessoa__cpfCnpj = forms.CharField(max_length=50, label="CNPJ")
#     # pessoa__rgIe = forms.CharField(max_length=50, label="Inscrição Estadual")
#     # pessoa__dataNascimento =  forms.DateField(label="Data Abertura")
#     # pessoa__endereco__descricao = forms.CharField(label="Descrição")
#     # pessoa__endereco__cep = forms.CharField(label="CEP")
#
#
#     class Meta:
#         model = Empresa
#         widgets = {'cpfCnpj': forms.TextInput(attrs={'data-mask': "000-000-0000"})}
#         # fields = ('nomeFantasia','logo')
#         fields = ('__all__')
#
#     def save(self, commit=True):
#
#         m = super(EmpresaForm, self).save(commit=False)
#         # do custom stuff
#         if commit:
#             m.save()
#         return m
#
