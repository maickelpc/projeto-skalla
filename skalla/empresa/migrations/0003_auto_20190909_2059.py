# Generated by Django 2.2.4 on 2019-09-09 23:59

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('empresa', '0002_colaborador_departamento'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='colaborador',
            options={'verbose_name': 'Colaborador', 'verbose_name_plural': 'Colaboradores'},
        ),
        migrations.AlterModelManagers(
            name='colaborador',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='colaborador',
            name='id',
        ),
        migrations.RemoveField(
            model_name='colaborador',
            name='usuario',
        ),
        migrations.AddField(
            model_name='colaborador',
            name='user_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
