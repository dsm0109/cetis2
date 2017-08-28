from django.forms import ModelForm
from django import forms
from .models import User

class FormUser(ModelForm):
    class Meta:
        model = User
        fields = ('imagen_perfil','first_name',
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
                  'nombre_tutor',
                                                 'direccion_tutor',
                                                 'ocupacion_tutor',
                                                 'trabajo_tutor',
                                                 'numeroUno_tutor',
                                                 'numeroDos_tutor',
                                                 )

        widgets = {
            'trabajo_tutor': forms.Textarea(),
        }


class FormClave(forms.Form):
    clave = forms.CharField(max_length=6, min_length=6)

class FormReglamento(forms.Form):
    acepto = forms.BooleanField(required=True, label="Acepto haber leído y me comprometo a respetar y hacer cumplir los lineamientos establecidos")