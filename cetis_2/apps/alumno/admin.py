from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cetis_2.apps.alumno.models import User
from django.contrib.auth.forms import UserChangeForm

class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            ('Información completa alumno', {'fields': ('imagen_perfil','first_name',
                                               'last_name',
                                                 'curp',
                                                 'sexo',
                                                 'turno',
                                                 'semestre',
                                                 'carrera',
                                                 'grupo',
                                                 'fecha_nacimiento',
                                                 'servicio_medico',
                                                 'des_servicio_medico',
                                                 'nss',
                                                 'domicilio',
                                                'colonia',
                                                        'delegacion',
                                                        'cp',
                                                 'numero_casa',
                                                 'numero_celular',
                                                 'email',
                                                 'tipo_sangre',
                                                 'alergias',
                                                 'enf_cronicas',
                                                 'medicamentos',
                                                 'impedimentos',
                                                 )}),
    ) + (
            ('Información tutor', {'fields': (   'nombre_tutor',
                                                 'direccion_tutor',
                                                 'ocupacion_tutor',
                                                 'trabajo_tutor',
                                                 'numeroUno_tutor',
                                                 'numeroDos_tutor',
                                                 )}),


    )+(
        ('Pasos', {'fields': ('paso_1',
                                          'paso_2',
                                          'paso_3',
                                          'paso_4',
                                         'fecha_cita',
                                        'code',
                                          )}),

    )

admin.site.register(User, MyUserAdmin)
admin.site.site_header = 'Reinscripcion Cetis 2'
