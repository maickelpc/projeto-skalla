from django.db import models

# Create your models here.
from django.db import models
from tenant_schemas.models import TenantMixin

class Cliente(TenantMixin):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    pago_ate = models.DateField()
    trial = models.BooleanField()
    cliente_desde = models.DateField(auto_now_add=True)
