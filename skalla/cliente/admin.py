from django.contrib import admin
from .models import Escala, Turno, Turno_PontoAlocacao, PontoAlocacao, Cliente, PerfilJornada, EscalaColaborador
from django import forms
from .models import Colaborador


class FormTurno(forms.ModelForm):
    periodo = forms.CharField(max_length=100)

    class Meta:
        model = Turno_PontoAlocacao
        fields = ['qtdeColaboradores','pontoAlocacao']




class TurnoAdmin(admin.ModelAdmin):
    list_display = ['id','descricao','descricao','horasTrabalhadas','horasDescanso','ativo']
    list_display_links = ['id','descricao','descricao','horasTrabalhadas','horasDescanso','ativo']
    search_fields = ['id','descricao','descricao','horasTrabalhadas','horasDescanso']


admin.site.register(Turno,TurnoAdmin)


admin.site.register(PerfilJornada)
admin.site.register(EscalaColaborador)

class PontoAlocacaoInline(admin.TabularInline):
    model = PontoAlocacao
    extra = 0
    max_num = 0
    readonly_fields = ['id', 'nome', 'descricao']
    fields = ['id', 'nome', 'descricao']
    can_delete = False




class Turno_PontoAlocacaoInline(admin.StackedInline):
    model = Turno_PontoAlocacao
    extra = 0
    autocomplete_fields = ['turno']
    form = FormTurno



class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id','nomeFantasia','nome','CNPJ','contatoEscala','telefone']
    list_display_links = ['id','nomeFantasia','CNPJ','nome','contatoEscala','telefone']
    search_fields = ['id','nomeFantasia','nome','CNPJ','contatoEscala','telefone']
    inlines = [PontoAlocacaoInline]


admin.site.register(Cliente, ClienteAdmin)



class PontoAlocacaoAdmin(admin.ModelAdmin):
    list_display = ['id','cliente','nome','cidade']
    list_display_links =  ['id','cliente','nome','cidade']
    search_fields = ['id','nome']
    ordering = ["cliente"]
    autoComplete = ['cliente']
    inlines = [Turno_PontoAlocacaoInline]


admin.site.register(PontoAlocacao, PontoAlocacaoAdmin)




class EscalaAdmin(admin.ModelAdmin):
    autocomplete_fields = ['turnoPonto','perfil']

admin.site.register(Escala)