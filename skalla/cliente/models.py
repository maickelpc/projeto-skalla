from django.db import models
from django.core.validators import MinValueValidator
from core.models import Endereco
from empresa.models import Colaborador

STATUS = (
    ( 0, 'AGENDADO'),
    (1, 'CONFIRMADO'),
    (2, 'CANCELADO')
)

# Create your models here.
class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=150, verbose_name="Razão Social")
    nomeFantasia = models.CharField(max_length=150, verbose_name="Nome Fantasia")
    CNPJ = models.CharField(max_length=20, unique=True, verbose_name="CNPJ")
    IE = models.CharField(max_length=30, unique=True, verbose_name="Inscrição Estadual")
    IM = models.CharField(max_length=30, unique=True, verbose_name="Inscrição Municipal", null=True)
    logo = models.ImageField(upload_to='logo', blank=True, verbose_name="Logotipo")
    endereco = models.ForeignKey(Endereco, related_name="endereco_cliente", on_delete=models.PROTECT, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, unique=True, verbose_name="Telefone")
    contatoEscala = models.CharField(max_length=50, unique=True, verbose_name="Contato para escalas")
    contatoEscalaFone = models.CharField(max_length=20, unique=True, verbose_name="Telefone contato para escalas")
    FinanceiroContato = models.CharField(max_length=50, unique=True, verbose_name="Contato financeiro")
    FinanceiroEmail = models.CharField(max_length=255, unique=True, verbose_name="Email financeiro")

    def __str__(self):
        return self.nomeFantasia

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['nomeFantasia']


class PontoAlocacao(models.Model):
    id = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente", related_name='cliente_ponto')
    nome = models.CharField(max_length=50, verbose_name="Ponto de Alocação")
    descricao = models.TextField( verbose_name="Descrição do Local")
    endereco = models.ForeignKey(Endereco, on_delete=models.PROTECT, verbose_name="Endereço")

    class Meta:
        verbose_name = "Ponto de Alocação"
        verbose_name_plural = "Pontos de Alocação"
        ordering = ['cliente','nome']
    def __str__(self):
        return self.cliente.nomeFantasia + ' - ' + self.nome


class Turno(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=50, verbose_name="Turno")
    periodo = models.CharField(max_length=50, verbose_name="Período")
    horasTrabalhadas = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)], verbose_name="Qtde de horas de trabalho")
    horasDescanso = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)], verbose_name="Qtde de horas de descanso")
    horaInicio = models.TimeField(verbose_name="Hora início do turno")
    horaFim = models.TimeField(verbose_name="Hora final do turno")
    ativo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos de trabalho"
        ordering = ['descricao']

    def __str__(self):
        return self.descricao


class Turno_PontoAlocacao(models.Model):
    id = models.AutoField(primary_key=True)

    turno = models.ForeignKey(Turno, on_delete=models.PROTECT, related_name="turno_ponto", verbose_name="Turno")
    pontoAlocacao = models.ForeignKey(PontoAlocacao, on_delete=models.PROTECT, related_name="ponto_turno", verbose_name="Ponto de Alocação")
    qtdeColaboradores = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)],verbose_name="Quantidade de colaboradores")


    def __str__(self):
        return self.turno.descricao + ' - ' + self.pontoAlocacao.nome

    class Meta:
        verbose_name = "Turno / Ponto de Alocação"
        verbose_name_plural = "Turno / Ponto de Alocação"
        unique_together = ['turno','pontoAlocacao']


class PerfilJornada(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=50, verbose_name="Descrição")
    tipo = models.CharField(max_length=50, verbose_name="Tipo")
    duplicar = models.BooleanField(default=False)
    horasAntecedenciaDuplicacao = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)], verbose_name="Horas de antecedencia para duplicar")

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = "Perfil de Jornada"
        verbose_name_plural = "Perfis de Jornada"


class Escala(models.Model):
    id = models.AutoField(primary_key=True)
    perfil = models.ForeignKey(PerfilJornada, on_delete=models.PROTECT,related_name='perfil_escala', verbose_name="Perfil de Jornada")
    turnoPonto = models.ForeignKey(Turno_PontoAlocacao, on_delete=models.PROTECT,related_name='turnoponto_escala', verbose_name="Turno / Ponto de alocação")
    dataInicio = models.DateTimeField()
    dataFim = models.DateTimeField()
    dataDuplicacao = models.DateTimeField()
    dataCancelamento = models.DateTimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.perfil.descricao + ' / ' + self.dataInicio.strftime("%d %m %Y %H:%M")

    class Meta:
        verbose_name = "Escala"
        verbose_name_plural = "Escalas"

class EscalaColaborador(models.Model):
    id = models.AutoField(primary_key=True)
    escala = models.ForeignKey(Escala, on_delete=models.PROTECT, related_name="escala_colaborador", verbose_name="Escala")
    colaborador = models.ForeignKey(Colaborador, on_delete=models.PROTECT, related_name="colaborador_escala", verbose_name="Colaborador")
    dataRegistro = models.DateTimeField(auto_now_add=True)
    dataConfirmacao = models.DateTimeField(null=True, blank=True)
    dataCancelamento = models.DateTimeField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS, default=0)