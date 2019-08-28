from django.db import models

# Create your models here.

from core.models import Endereco


class Pessoa(models.Model):

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    cpf_cnpj = models.CharField(max_length=20, unique=True)
    rg_ie = models.CharField(max_length=20, unique=True)
    # inscMunicipal = models.CharField(max_length=20, unique=True, null=True, blank=True)
    dataNascimento = models.DateField()
    endereco = models.OneToOneField(Endereco, on_delete=models.PROTECT, primary_key=False)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural ="Pessoas"
        ordering = ['nome']


class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    contato = models.CharField(max_length=11, null=True, blank=True)
    contato_financeiro = models.CharField(max_length=11)
    insc_municipal = models.CharField(max_length=20, unique=True, null=True, blank=True)
    pessoa = models.OneToOneField(Pessoa, on_delete=models.PROTECT)

    def __str__(self):
        return self.pessoa.nome

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Usuario(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    senha = models.CharField(max_length=150)
    ativo = models.BooleanField(default=False)
    pessoa = models.OneToOneField(Pessoa, on_delete=models.PROTECT)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


