# Generated by Django 2.2.5 on 2019-10-01 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0008_auto_20191001_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='escalacolaborador',
            name='statusSolicitacao',
            field=models.SmallIntegerField(blank=True, null=True),
        ),
    ]