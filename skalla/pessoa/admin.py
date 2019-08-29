from django.contrib import admin

# Register your models here.
from pessoa.models import Pessoa, Cliente, Usuario


class ClienteAdminInline(admin.TabularInline):
    model = Cliente
    extra = 0


class UsuarioAdminInline(admin.TabularInline):
    model = Usuario
    extra = 0

class PessoaAdminInline(admin.StackedInline):
    model = Pessoa
    extra = 0


class PessoaAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'cpf_cnpj']
    list_display = ['id', 'nome', 'sobrenome']
    list_display_links = ['nome', 'sobrenome']
    inlines = [UsuarioAdminInline, ClienteAdminInline]


admin.site.register(Pessoa, PessoaAdmin)


class ClienteAdmin(admin.ModelAdmin):
    search_fields = ['insc_municipal']


admin.site.register(Cliente, ClienteAdmin)


class UsuarioAdmin(admin.ModelAdmin):
    search_fields = ['email', 'ativo']


admin.site.register(Usuario, UsuarioAdmin)