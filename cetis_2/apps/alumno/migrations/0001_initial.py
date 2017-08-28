# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-15 07:05
from __future__ import unicode_literals

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('imagen_perfil', models.ImageField(default='user-default.png', upload_to='', verbose_name='Imagen de perfil')),
                ('first_name', models.CharField(max_length=40, null=True, verbose_name='Nombre(s)')),
                ('last_name', models.CharField(max_length=40, null=True, verbose_name='Apellidos')),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=20, null=True, verbose_name='Sexo')),
                ('curp', models.CharField(help_text='La Clave Única de Registro de Población (CURP) es un código alfanumérico único de identidad de 18 caracteres', max_length=18, null=True, unique=True, verbose_name='CURP')),
                ('turno', models.CharField(choices=[('Matutino', 'Matutino'), ('Vespertino', 'Vespertino')], max_length=10, null=True, verbose_name='Turno')),
                ('semestre', models.CharField(choices=[('Primero', 'Primero'), ('Tercero', 'Tercero'), ('Quinto', 'Quinto')], max_length=7, null=True, verbose_name='Semestre')),
                ('carrera', models.CharField(choices=[('Admistración de Recurso Humanos', 'Admistración de Recurso Humanos'), ('Arquitectura', 'Arquitectura'), ('Diseño Decorativo', 'Diseño Decorativo'), ('Diseño Industrial', 'Diseño Industrial')], max_length=50, null=True, verbose_name='Carrera')),
                ('grupo', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], max_length=1, null=True, verbose_name='Grupo')),
                ('fecha_nacimiento', models.DateField(null=True, verbose_name='Fecha de nacimiento')),
                ('servicio_medico', models.CharField(choices=[('Si', 'Si'), ('No', 'No')], max_length=2, null=True, verbose_name='¿Cuenta con algún servicio médico?')),
                ('des_servicio_medico', models.CharField(blank=True, help_text='Únicamente en caso de contar con servicio médico', max_length=300, null=True, verbose_name='¿Cuál es su servicio médico?')),
                ('nss', models.CharField(blank=True, max_length=50, null=True, verbose_name='Número de Seguridad Social (NSS)')),
                ('domicilio', models.TextField(help_text='Calle, Número Exterior, Número interior', null=True, verbose_name='Dirección')),
                ('colonia', models.CharField(max_length=200, null=True, verbose_name='Colonia')),
                ('delegacion', models.CharField(choices=[('Álvaro Obregón', 'Álvaro Obregón'), ('Azcapotzalco', 'Azcapotzalco'), ('Benito Juárez', 'Benito Juárez'), ('Coyoacán', 'Coyoacán'), ('Cuajimalpa de Morelos', 'Cuajimalpa de Morelos'), ('Cuauhtémoc', 'Cuauhtémoc'), ('Gustavo A. Madero', 'Gustavo A. Madero'), ('Iztacalco', 'Iztacalco'), ('Iztapalapa', 'Iztapalapa'), ('Magdalena Contreras', 'Magdalena Contreras'), ('Miguel Hidalgo', 'Miguel Hidalgo'), ('Milpa Alta', 'Milpa Alta'), ('Tláhuac', 'Tláhuac'), ('Tlalpan', 'Tlalpan'), ('Venustiano Carranza', 'Venustiano Carranza'), ('Xochimilco', 'Xochimilco'), ('Atizapán', 'Atizapán'), ('Atlacomulco', 'Atlacomulco'), ('Ecatepec', 'Ecatepec'), ('Naucalpan', 'Naucalpan'), ('Nezahualcóyotl', 'Nezahualcóyotl'), ('Tenango', 'Tenango'), ('Texcoco', 'Texcoco'), ('Toluca', 'Toluca'), ('Valle de Bravo', 'Valle de Bravo')], max_length=100, null=True, verbose_name='Delegación')),
                ('cp', models.CharField(max_length=10, null=True, verbose_name='Código Postal')),
                ('numero_casa', models.CharField(help_text='8 digitos', max_length=8, null=True, verbose_name='Teléfono de casa')),
                ('numero_celular', models.CharField(help_text='13 digitos, con el prefijo 04455', max_length=13, null=True, verbose_name='Teléfono celular')),
                ('email', models.EmailField(max_length=254, null=True, verbose_name='Correo electrónico')),
                ('tipo_sangre', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], max_length=3, null=True, verbose_name='Tipo de sangre')),
                ('alergias', models.TextField(blank=True, default='Ninguna', max_length=300, null=True, verbose_name='Alergias')),
                ('enf_cronicas', models.TextField(blank=True, default='Ninguna', max_length=300, null=True, verbose_name='Padecimientos o enfermedades crónicas')),
                ('medicamentos', models.TextField(blank=True, default='Ninguno', max_length=300, null=True, verbose_name='Medicamentos que toma de forma permanente')),
                ('impedimentos', models.TextField(blank=True, default='Ninguno', max_length=200, null=True, verbose_name='Impedimentos')),
                ('nombre_tutor', models.CharField(max_length=100, null=True, verbose_name='Nombre completo del tutor')),
                ('direccion_tutor', models.TextField(help_text='Calle, Número Exterior, Lote, Colonia, Municipio, C.P. Estado', null=True, verbose_name='Dirección del tutor')),
                ('ocupacion_tutor', models.CharField(max_length=100, null=True, verbose_name='Ocupación del tutor')),
                ('trabajo_tutor', models.TextField(null=True, verbose_name='Direccion del trabajo')),
                ('numeroUno_tutor', models.CharField(help_text='Puede ser télefono de casa o celular', max_length=13, null=True, verbose_name='Télefono de contacto del tutor')),
                ('numeroDos_tutor', models.CharField(help_text='Puede ser télefono de casa o celular', max_length=13, null=True, verbose_name='Otro télefono de contacto')),
                ('paso_1', models.BooleanField(default=False, verbose_name='Paso 1')),
                ('paso_2', models.BooleanField(default=False, verbose_name='Paso 2')),
                ('paso_3', models.BooleanField(default=False, verbose_name='Paso 3')),
                ('paso_4', models.BooleanField(default=False, verbose_name='Paso 4')),
                ('fecha_cita', models.DateTimeField(blank=True, null=True, verbose_name='Fecha cita')),
                ('code', models.CharField(blank=True, max_length=6, null=True, verbose_name='Código')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]