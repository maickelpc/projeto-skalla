# Generated by Django 2.2.5 on 2019-09-17 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0005_auto_20190911_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pontoalocacao',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_ponto', to='cliente.Cliente', verbose_name='Cliente'),
        ),
    ]
