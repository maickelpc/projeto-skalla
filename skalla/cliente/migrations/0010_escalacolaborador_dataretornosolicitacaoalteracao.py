# Generated by Django 2.2.5 on 2019-10-01 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0009_escalacolaborador_statussolicitacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='escalacolaborador',
            name='dataRetornoSolicitacaoAlteracao',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
