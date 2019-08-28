from django.contrib import admin
from .models import Pais, Estado, Cidade, Endereco

# Register your models here.


class EstadoAdminInline(admin.TabularInline):
    model = Estado
    extra = 0


class CidadeAdminInline(admin.TabularInline):
    model = Cidade
    extra = 0

class PaisAdminInline(admin.TabularInline):
    model = Pais
    extra = 0


class PaisAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    inlines = [EstadoAdminInline]
    list_display = ['id', 'nome']
    list_display_links = ['nome']


admin.site.register(Pais, PaisAdmin)


class EstadoAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ['id','nome', 'pais']
    list_display_links = ['id', 'nome', 'pais']
    autocomplete_fields = ['pais']
    inlines = [CidadeAdminInline]


admin.site.register(Estado, EstadoAdmin)


class CidadeAdmin(admin.ModelAdmin):
    search_fields = ['nome']
    list_display = ['id','nome', 'estado']
    list_display_links = ['id', 'nome', 'estado']
    autocomplete_fields = ['estado']


admin.site.register(Cidade, CidadeAdmin)


class EnderecoAdmin(admin.ModelAdmin):
    search_fields = ['logradouro', 'bairro']
    list_display = ['id', 'logradouro', 'bairro', 'cidade']
    list_display_links = ['logradouro', 'bairro']
    autocomplete_fields = ['cidade']


admin.site.register(Endereco, EnderecoAdmin)