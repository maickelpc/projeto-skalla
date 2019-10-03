# Generated by Django 2.2.4 on 2019-09-30 23:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0007_auto_20190930_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfiljornada',
            name='dias',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
