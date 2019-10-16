from django.db import models
from django.contrib.auth.models import  Group
# Create your models here.

class Pais(models.Model):
    id = models.AutoField(primary_key=True )
    nome = models.CharField(max_length=20)
    sigla = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Pais"
        verbose_name_plural ="Paises"
        ordering = ['nome']


class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=20)
    sigla = models.CharField(max_length=3)
    pais = models.ForeignKey( Pais, on_delete=models.PROTECT, related_name='pais')

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        ordering = ['id', 'nome', 'sigla']
        unique_together = ('pais', 'sigla')


class Cidade(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    codigoIbge = models.CharField(max_length=10, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='estado')

    def __str__(self):
        return self.nome + ' / ' +self.estado.sigla

    def pais(self):
        return self.estado.pais.nome

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        ordering = ['estado','nome']
        unique_together = ('estado', 'nome')


# class Endereco(models.Model):
#     id = models.AutoField(primary_key=True)
#     descricao = models.CharField(max_length=20)
#     cep = models.CharField(max_length=10)
#     logradouro = models.CharField(max_length=50)
#     numero = models.CharField(max_length=6)
#     bairro = models.CharField(max_length=50)
#     complemento = models.CharField(max_length=100, null=True, blank=True)
#     referencia = models.CharField(max_length=100, null=True, blank=True)
#     cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, related_name='cidade')
#
#     def __str__(self):
#         return self.descricao
#
#     class Meta:
#         verbose_name = "Endereço"
#         verbose_name_plural = "Endereços"


class Configuracao(models.Model):
    id = models.AutoField(primary_key=True)
    grupoColaborador = models.ForeignKey(Group, related_name='grupo_colaborador', on_delete=models.PROTECT, verbose_name="Grupo dos Colaboradores", blank=True, null=True)
    grupoGestor = models.ForeignKey(Group, related_name='grupo_administrador', on_delete=models.PROTECT, verbose_name="Grupo dos Adminstradores", blank=True, null=True )
    grupoUsuarios = models.ForeignKey(Group, related_name='grupo_Usuario', on_delete=models.PROTECT, verbose_name="Grupo dos Usuários", blank=True, null=True )

    class Meta:
        verbose_name = "Configurações"
        verbose_name_plural = "Configurações"