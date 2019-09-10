from django.db import models
from django.core.validators import MinValueValidator
from core.models import Endereco
from django.contrib.auth.models import User

# Create your models here.
class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150, verbose_name="Razão Social")
    nomeFantasia = models.CharField(max_length=150, verbose_name="Nome Fantasia")
    CNPJ = models.CharField(max_length=20, unique=True, verbose_name="CNPJ")
    IE = models.CharField(max_length=20, unique=True, verbose_name="Inscrição Estadual")
    logo = models.ImageField(upload_to='logo', blank=True, verbose_name="Logotipo")
    endereco = models.ForeignKey(Endereco, related_name="endereco_empresa", on_delete=models.PROTECT, verbose_name="Endereço")
    dataAbertura = models.DateField(verbose_name="Data de Abertura")

    def __str__(self):
        return self.nomeFantasia

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nomeFantasia']


class Area(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, verbose_name="Área")
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT,related_name="user_area", verbose_name="Usuário Responsável")

    class Meta:
        verbose_name = "Área"
        verbose_name_plural = "Áreas"
        ordering = ['nome']
    def __str__(self):
        return self.nome


class Departamento(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50, verbose_name="Área")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="area_departamento", verbose_name="Área")
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT,related_name="user_departamento", verbose_name="Usuário Responsável")

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ['area','nome']

    def __str__(self):
        return self.area.nome + ' - ' + self.nome

class Colaborador(User):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="empresa_area", verbose_name="Empresa")
    dataNascimento = models.DateField(verbose_name="Data de Nascimento")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    celular = models.CharField(max_length=20, verbose_name="Celular")
    contato = models.CharField(max_length=20, verbose_name="Contato")
    contatoFone = models.CharField(max_length=20, verbose_name="Telefone Contato")
    dataAdmissao = models.DateField(verbose_name="Data Admissão")
    PIS = models.CharField(max_length=20)
    departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT, related_name='depto_colaborador', verbose_name='Departamento')
    limiteHorasMes = models.SmallIntegerField( validators=[MinValueValidator(1)], verbose_name="Máximo de horas de trabalho mensal")
    limiteHorasSemana = models.SmallIntegerField(validators=[MinValueValidator(1)], verbose_name="Máximo de horas de trabalho semanal")

    def __str__(self):
        return self.first_name

    def nome(self):
        return self.first_name

    def sobrenome(self):
        return self.last_name

    def email(self):
        return self.email


    class Meta:
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"
        # ordering = ['usuario__name']


class PeriodoInativo(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=100)
    colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE, related_name="colaborador_periodo", verbose_name="Colaborador")
    dataRegistro = models.DateTimeField(auto_now_add=True)
    dataInicio = models.DateField(verbose_name="Data início")
    dataFim = models.DateField(verbose_name="Data Fim")
    usuarioRegistro = models.CharField(max_length=150, verbose_name="Registrado Por")

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Período de Inatividade"
        verbose_name_plural = "Períodos de Inatividade"
        ordering = ['dataRegistro']