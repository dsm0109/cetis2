from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    TURNOS = (
        ('Matutino', 'Matutino'),
        ('Vespertino', 'Vespertino'),
    )

    SERVICIO_MEDICO = (
        ('Si', 'Si'),
        ('No', 'No'),
    )

    TIPO_SANGRE = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )

    SEMESTRES = (
        ('Tercero', 'Tercero'),
        ('Quinto', 'Quinto'),
    )

    CARRERAS = (
        ('Administración de Recursos Humanos', 'Administración de Recursos Humanos'),
        ('Arquitectura', 'Arquitectura'),
        ('Diseño Decorativo', 'Diseño Decorativo'),
        ('Diseño Industrial', 'Diseño Industrial'),
    )

    GRUPOS = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    SEXO = (
        ('M','Masculino'),
        ('F', 'Femenino')
    )

    DELEGACIONES = (
        ('Álvaro Obregón','Álvaro Obregón'),
        ('Azcapotzalco', 'Azcapotzalco'),
        ('Benito Juárez', 'Benito Juárez'),
        ('Coyoacán', 'Coyoacán'),
        ('Cuajimalpa de Morelos', 'Cuajimalpa de Morelos'),
        ('Cuauhtémoc', 'Cuauhtémoc'),
        ('Gustavo A. Madero', 'Gustavo A. Madero'),
        ('Iztacalco', 'Iztacalco'),
        ('Iztapalapa', 'Iztapalapa'),
        ('Magdalena Contreras', 'Magdalena Contreras'),
        ('Miguel Hidalgo', 'Miguel Hidalgo'),
        ('Milpa Alta', 'Milpa Alta'),
        ('Tláhuac', 'Tláhuac'),
        ('Tlalpan', 'Tlalpan'),
        ('Venustiano Carranza', 'Venustiano Carranza'),
        ('Xochimilco', 'Xochimilco'),
        ('Atizapán', 'Atizapán'),
        ('Atlacomulco', 'Atlacomulco'),
        ('Chalco', 'Chalco'),
        ('Cuautitlán', 'Cuautitlán'),
        ('Ecatepec', 'Ecatepec'),
        ('Naucalpan', 'Naucalpan'),
        ('Nezahualcóyotl', 'Nezahualcóyotl'),
        ('Tenango', 'Tenango'),
        ('Texcoco', 'Texcoco'),
        ('Toluca', 'Toluca'),
        ('Valle de Bravo', 'Valle de Bravo'),
        ('Valle de Chalco', 'Valle de Chalco'),
    )



    imagen_perfil = models.ImageField(upload_to='', null=False, blank=False, default='user-default.png', verbose_name='Imagen de perfil')

    first_name = models.CharField(max_length=40,
                                 null=True,
                                 blank=False,
                                 verbose_name='Nombre(s)')

    last_name = models.CharField(max_length=40,
                                  null=True,
                                  blank=False,
                                  verbose_name='Apellidos')

    sexo = models.CharField(max_length=20, choices=SEXO, null=True, blank=False, verbose_name='Sexo')

    curp = models.CharField(max_length=18,
                            null=True,
                            blank=False,
                            unique=True,
                            help_text="La Clave Única de Registro de Población (CURP) es un código alfanumérico único "
                                      "de identidad de 18 caracteres",
                            verbose_name='CURP')

    turno = models.CharField(max_length=10,
                             choices=TURNOS,
                             null=True,
                             blank=False,
                             verbose_name='Turno')

    semestre = models.CharField(max_length=7,
                                choices=SEMESTRES,
                                null=True,
                                blank=False,
                                verbose_name='Semestre')

    carrera = models.CharField(max_length=50,
                               choices=CARRERAS,
                               null=True,
                               blank=False,
                               verbose_name='Carrera')

    grupo = models.CharField(max_length=1,
                             choices=GRUPOS,
                             null=True,
                             blank=False,
                             verbose_name='Grupo')

    fecha_nacimiento = models.DateField(auto_now=False,
                                        auto_now_add=False,
                                        null=True,
                                        blank=False,
                                        verbose_name='Fecha de nacimiento',
                                        help_text='dd/mm/aaaa')

    servicio_medico = models.CharField(max_length=2,
                                       choices=SERVICIO_MEDICO,
                                       null=True,
                                       blank=False,
                                       verbose_name='¿Cuenta con algún servicio médico?')

    des_servicio_medico = models.CharField(max_length=300,
                                           null=True,
                                           blank=True,
                                           verbose_name='¿Cuál es su servicio médico?',
                                           help_text='Únicamente en caso de contar con servicio médico',
                                           default=' - ')

    nss = models.CharField(max_length=50,
                           null=True,
                           blank=True,
                           verbose_name='Número de Seguridad Social (NSS)', default=' - ')

    domicilio = models.TextField(null=True,
                                 blank=False,
                                 verbose_name='Dirección',
                                 help_text='Calle, Número Exterior, Número interior'
                                 )

    colonia = models.CharField(max_length=200, null=True, blank=False, verbose_name='Colonia')

    delegacion = models.CharField(max_length=100, choices=DELEGACIONES ,null=True, blank=False, verbose_name='Delegación')

    cp = models.CharField(max_length=10, null=True, blank=False, verbose_name='Código Postal')

    numero_casa = models.CharField(max_length=8,
                                   null=True,
                                   blank=False,
                                   verbose_name='Teléfono de casa',
                                   help_text='8 digitos')

    numero_celular = models.CharField(max_length=13,
                                      null=True,
                                      blank=False,
                                      verbose_name='Teléfono celular',
                                      help_text='13 digitos, con el prefijo 04455')

    email = models.EmailField(verbose_name='Correo electrónico', null=True, blank=False)

    tipo_sangre = models.CharField(max_length=3,
                                   choices=TIPO_SANGRE,
                                   null=True,
                                   blank=False,
                                   verbose_name='Tipo de sangre')

    alergias = models.TextField(max_length=300,
                                null=True,
                                blank=True,
                                default='Ninguna',
                                verbose_name='Alergias')

    enf_cronicas = models.TextField(max_length=300,
                                    null=True,
                                    blank=True,
                                    default='Ninguna',
                                    verbose_name='Padecimientos o enfermedades crónicas')

    medicamentos = models.TextField(max_length=300,
                                    null=True,
                                    blank=True,
                                    default='Ninguno',
                                    verbose_name='Medicamentos que toma de forma permanente')

    impedimentos = models.TextField(max_length=200, null=True, blank=True, default='Ninguno',
                                    verbose_name='Impedimentos')

    nombre_tutor = models.CharField(max_length=100,
                                    null=True,
                                    blank=False,
                                    verbose_name='Nombre completo del tutor')

    direccion_tutor = models.TextField(
                                    null=True,
                                    blank=False,
                                    verbose_name='Dirección del tutor',
                                    help_text='Calle, Número Exterior, Lote, Colonia, Municipio, C.P. Estado')

    ocupacion_tutor = models.CharField(max_length=100,
                                       null=True,
                                       blank=False,
                                       verbose_name='Ocupación del tutor')

    trabajo_tutor = models.TextField(null=True, blank=False, verbose_name='Dirección del trabajo')

    numeroUno_tutor = models.CharField(max_length=13,
                                       null=True,
                                       blank=False,
                                       verbose_name='Télefono de contacto del tutor',
                                       help_text='Puede ser tléfono de casa o celular')

    numeroDos_tutor = models.CharField(max_length=13,
                                       null=True,
                                       blank=False,
                                       verbose_name='Otro télefono de contacto',
                                       help_text='Puede ser teléfono de casa o celular')

    paso_1 = models.BooleanField(default=False, verbose_name='Paso 1', blank=True, null=False, editable=True)

    paso_2 = models.BooleanField(default=False, verbose_name='Paso 2', blank=True, null=False, editable=True)

    paso_3 = models.BooleanField(default=False, verbose_name='Paso 3', blank=True, null=False, editable=True)

    paso_4 = models.BooleanField(default=False, verbose_name='Paso 4', blank=True, null=False, editable=True)

    fecha_cita = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name='Fecha cita')

    code = models.CharField(max_length=6, null=True, blank=True, verbose_name='Código')

