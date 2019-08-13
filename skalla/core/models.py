from django.db import models

# Create your models here.

class ClienteSistema(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)