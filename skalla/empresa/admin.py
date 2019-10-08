from django_reverse_admin import ReverseModelAdmin
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Empresa, Area, Departamento, Colaborador, PeriodoInativo
from .forms import ColaboradorForm

# Register your models here.
# class EnderecoInline(admin.StackedInline):
#     model = Endereco
#     extra = 1
#     max_num = 1
#     autocomplete_fields = ['cidade']

class AreaInline(admin.TabularInline):
    model = Area
    extra = 0
    autocomplete_fields = ['responsavel']

class DepartamentoInline(admin.TabularInline):
    model = Departamento
    extra = 0
    autocomplete_fields = ['responsavel']

class ColaboradorInline(admin.TabularInline):
    model = Colaborador
    extra = 0
    max_num = 0
    readonly_fields = ['id','nome','sobrenome','email']
    fields = ['id','nome','sobrenome','email']
    can_delete = False


class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['id','nome', 'nomeFantasia','CNPJ']
    list_display_links = ['id', 'nome', 'nomeFantasia', 'CNPJ']
    search_fields = ['id', 'nome', 'nomeFantasia', 'CNPJ']
    inlines = [ColaboradorInline]

admin.site.register(Empresa, EmpresaAdmin)


class AreaAdmin(admin.ModelAdmin):
    list_display = ['nome','responsavel']
    list_display_links = ['nome', 'responsavel']
    search_fields = ['nome']
    ordering = ['nome']
    list_select_related = ['responsavel']
    inlines = [DepartamentoInline]

admin.site.register(Area, AreaAdmin)

class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['area','nome','responsavel']
    list_display_links = ['area', 'nome', 'responsavel']
    search_fields = ['nome']
    ordering = ['area','nome']
    list_select_related = ['responsavel']
    autocomplete_fields = ['area','responsavel']
    inlines = [ColaboradorInline]

admin.site.register(Departamento, DepartamentoAdmin)


class PeriodoInativoInline(admin.TabularInline):
    model = PeriodoInativo
    can_delete = False
    extra = 0

class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','departamento','email']
    list_display_links = ['id','first_name','last_name','departamento','email']
    search_fields = ['id','first_name','last_name','departamento','email']
    autocomplete_fields = ['departamento','empresa']
    form = ColaboradorForm
    inlines = [PeriodoInativoInline]

admin.site.register(Colaborador, ColaboradorAdmin)