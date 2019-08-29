from django_reverse_admin import ReverseModelAdmin
from pessoa.admin import PessoaAdminInline
from django.contrib import admin

from .forms import EmpresaForm
from .models import  Empresa

# Register your models here.

# class EmpresaAdmin(ReverseModelAdmin):
class EmpresaAdmin(admin.ModelAdmin):
    search_fields = ['empresa.nome','nomeFantasia']
    # inline_reverse = [('pessoa', {'inlines': ['endereco']})]
    # inline_type = 'stacked'
    form = EmpresaForm
    # inlines = []
    # list_display = ['id', 'empresa.nome','nomeFantasia']
    # list_display_links = ['id', 'empresa.nome','nomeFantasia']


admin.site.register(Empresa, EmpresaAdmin)