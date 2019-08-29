from pessoa.models import Pessoa
from django.db import models

# Create your models here.
class Empresa(models.Model):
    id = models.AutoField(primary_key=True)
    nomeFantasia = models.CharField(max_length=150, verbose_name="Nome Fantasia")
    logo = models.ImageField(upload_to='logo', blank=True, verbose_name="Logotipo")
    pessoa = models.OneToOneField(Pessoa, on_delete=models.PROTECT, related_name='pessoa')

    def __str__(self):
        return self.nomeFantasia

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ['nomeFantasia']

