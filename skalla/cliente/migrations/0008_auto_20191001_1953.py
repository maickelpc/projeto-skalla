# Generated by Django 2.2.5 on 2019-10-01 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0007_auto_20190930_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='escalacolaborador',
            name='dataSolicitacaoAlteracao',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='escalacolaborador',
            name='solicitacaoAlteracao',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]