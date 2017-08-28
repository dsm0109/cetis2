# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-19 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumno', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='carrera',
            field=models.CharField(choices=[('Administración de Recursos Humanos', 'Administración de Recursos Humanos'), ('Arquitectura', 'Arquitectura'), ('Diseño Decorativo', 'Diseño Decorativo'), ('Diseño Industrial', 'Diseño Industrial')], max_length=50, null=True, verbose_name='Carrera'),
        ),
        migrations.AlterField(
            model_name='user',
            name='des_servicio_medico',
            field=models.CharField(blank=True, default=' - ', help_text='Únicamente en caso de contar con servicio médico', max_length=300, null=True, verbose_name='¿Cuál es su servicio médico?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='fecha_nacimiento',
            field=models.DateField(help_text='dd/mm/aaaa', null=True, verbose_name='Fecha de nacimiento'),
        ),
        migrations.AlterField(
            model_name='user',
            name='nss',
            field=models.CharField(blank=True, default=' - ', max_length=50, null=True, verbose_name='Número de Seguridad Social (NSS)'),
        ),
        migrations.AlterField(
            model_name='user',
            name='semestre',
            field=models.CharField(choices=[('Tercero', 'Tercero'), ('Quinto', 'Quinto')], max_length=7, null=True, verbose_name='Semestre'),
        ),
    ]
