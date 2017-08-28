from cetis_2.apps.alumno.form import FormUser
from cetis_2.apps.alumno.form import FormClave
from cetis_2.apps.alumno.form import FormReglamento
from cetis_2.apps.alumno.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from django.http import HttpResponse
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import datetime
from datetime import timedelta
import locale
import sys


@login_required
def inicio(request):
    instancia = User.objects.get(id=request.user.id)
    lista = [0, 0]
    contador = 0
    if instancia.paso_1 == True:
        contador += 25
    if instancia.paso_2 == True:
        contador += 25
    if instancia.paso_3 == True:
        contador += 25
    if instancia.paso_4 == True:
        contador += 25

    lista[0] = contador
    lista[1] = 100 - contador

    return render(request, 'inicio.html', {'datos': lista, })


@login_required
def mi_info(request):
    instancia = User.objects.get(id=request.user.id)
    if (instancia.paso_1 is False) and (instancia.nombre_tutor is not None):
        instancia.paso_1 = True
        instancia.save()

    if instancia.paso_1 == True:
        return render(request, 'yo.html', {})
    else:
        return redirect(reverse_lazy('editar'))


@login_required
def reglamento(request):
    instancia = User.objects.get(id=request.user.id)
    formulario = FormReglamento()

    bandera = False
    if instancia.paso_1 == True and instancia.paso_2 == True:
        bandera = True
    if request.method == 'POST':

        formulario = FormReglamento(request.POST)
        if True:
            c = request.POST.get("acepto", None)

            if str(c) == "on":
                instancia.paso_3 = True;
                instancia.save()
                return redirect(reverse_lazy('reglamento'))
            else:
                return render(request, 'reglamento.html', {'bandera': bandera, 'form': formulario, 'alerta': True, })
    else:
        return render(request, 'reglamento.html', {'bandera': bandera, 'form': formulario, 'alerta': False, })

    return render(request, 'reglamento.html', {'bandera': bandera, 'form':formulario})


@login_required
def cita(request):
    instancia = User.objects.get(id=request.user.id)
    bandera = False
    if instancia.paso_1 == True and instancia.paso_2 == True and instancia.paso_3 == True:
        bandera = True
    return render(request, 'cita.html', {'bandera': bandera, })


@login_required
def pago(request):
    instancia = User.objects.get(id=request.user.id)
    formulario = FormClave()
    bandera = False
    if instancia.paso_1 == True:
        bandera = True

    if request.method == 'POST':
        formulario = FormClave(request.POST)
        if formulario.is_valid():
            c = formulario.cleaned_data['clave']

            if str(c) == str(instancia.code):
                instancia.paso_2 = True;
                instancia.save()
                return redirect(reverse_lazy('pago'))
            else:
                return render(request, 'pago.html', {'bandera': bandera, 'form': formulario, 'alerta': True, })
    else:
        return render(request, 'pago.html', {'bandera': bandera, 'form': formulario, 'alerta': False, })

    return render(request, 'pago.html', {'bandera': bandera, 'form': formulario, 'alerta': False, })


@login_required
def editar(request):
    if request.method == 'POST':
        formulario = FormUser(request.POST, request.FILES, instance=request.user)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            usuario.User = User.objects.get(id=request.user.id)
            im = Image.open(usuario.imagen_perfil)
            output = BytesIO()
            im.thumbnail((512, 512), Image.ANTIALIAS)
            longer_side = max(im.size)
            horizontal_padding = (longer_side - im.size[0]) / 2
            vertical_padding = (longer_side - im.size[1]) / 2
            img_new = im.crop(
                (
                    -horizontal_padding,
                    -vertical_padding,
                    im.size[0] + horizontal_padding,
                    im.size[1] + vertical_padding
                )
            )
            img_new.save(output, format='JPEG', quality=100)
            output.seek(0)
            usuario.imagen_perfil = InMemoryUploadedFile(output, 'ImageField',
                                                         "%s.jpg" % usuario.imagen_perfil.name.split('.')[0],
                                                         'image/jpeg',
                                                         sys.getsizeof(output), None)
            usuario.save()
            return redirect(reverse_lazy('mi_info'))
        else:
            instance = User.objects.get(id=request.user.id)
            formulario = FormUser(instance=instance)
            return render(request, 'editar.html', {'form': formulario,'aviso': True})
    else:
        instance = User.objects.get(id=request.user.id)
        formulario = FormUser(instance=instance)
        return render(request, 'editar.html', {'form': formulario,
                                               })


def log_in(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy('inicio'))
    if request.method == 'POST':
        usuario = request.POST.get('usuario', '')
        passw = request.POST.get('pass', '')
        user = authenticate(username=usuario, password=passw)
        if user is not None:
            login(request, user)
            return redirect(reverse_lazy('inicio'))
        else:
            return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})
    return render(request, 'login.html', {})


@login_required
def log_out(request):
    logout(request)
    return redirect(reverse_lazy('login'))


@login_required
def download_inscripcion(request):
    instancia = User.objects.get(id=request.user.id)

    if instancia.paso_1 == True and instancia.paso_2 == True and instancia.paso_3 == True and instancia.paso_4 == False:
        instancia.paso_4 = True;
        instancia.save()

    if instancia.paso_1 == True and instancia.paso_2 == True and instancia.paso_3 == True and instancia.paso_4 == True:
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}-solicitud-inscripcion.pdf"'.format(str(instancia.username))
        buffer = BytesIO()
        #Config canvas
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        p.translate(inch,inch)
        p.setStrokeColorRGB(0, 0, 0)
        p.setFillColorRGB(0, 0, 0)

        #Draw canvas

        #Cabecera
        p.setFont('Helvetica-Bold', 11)
        p.drawCentredString(3.2 * inch, 9.5 * inch, 'DIRECCIÓN GENERAL DE EDUCACIÓN TECNOLÓGICA INDUSTRIAL')
        p.drawCentredString(3.2 * inch, 9.3 * inch, 'CENTRO DE ESTUDIOS TECNOLÓGICOS INDUSTRIAL Y DE SERVICIOS No. 2')
        p.drawCentredString(3.2 * inch, 9.1 * inch, '“DAVID ALFARO SIQUEIROS”')
        p.setFont('Helvetica-Bold', 13)
        p.drawCentredString(3.2 * inch, 8 * inch, 'SOLICITUD DE INSCRIPCIÓN')
        p.setFont('Helvetica', 12)
        p.drawCentredString(3.2 * inch, 7.8 * inch, 'SEMESTRE AGOSTO 2017 – ENERO 2018')
        dgeti = ImageReader('{}/img/dgeti_pdf.png'.format(settings.STATICFILES_DIRS[0]))
        p.drawImage(dgeti, 5.5 * inch,8 * inch, width=60, height=73, mask=None)

        #Datos box
        p.rect(-0.4 * inch, 6.75 * inch, 7.3 * inch, 0.8 * inch, stroke=1, fill=0)
        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 7.3 * inch, 'NÚMERO DE CONTROL:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(1.5 * inch, 7.3 * inch, '{}'.format(str(instancia.username).upper()))
        p.setFont('Helvetica', 10)
        p.drawString(2.9 * inch, 7.3 * inch, 'CARRERA:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(3.7 * inch, 7.3 * inch, '{}'.format(str(instancia.carrera).upper()))
        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 6.9 * inch, 'SEMESTRE:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(0.7 * inch, 6.9 * inch, '{}'.format(str(instancia.semestre).upper()))
        p.setFont('Helvetica', 10)
        p.drawString(2.6 * inch, 6.9 * inch, 'GRUPO:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(3.2 * inch, 6.9 * inch, '{}'.format(str(instancia.grupo).upper()))
        p.setFont('Helvetica', 10)
        p.drawString(4.5 * inch, 6.9 * inch, 'TURNO:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(5.1 * inch, 6.9 * inch, '{}'.format(str(instancia.turno).upper()))

        # DATOS DEL SOLICITANTE
        p.setFont('Helvetica-Bold', 11)
        p.drawCentredString(3.2 * inch, 6.4 * inch, 'DATOS DEL SOLICITANTE')

        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 6 * inch, 'NOMBRE:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(0.5 * inch, 6 * inch, '{} {}'.format(str(instancia.first_name).upper(), str(instancia.last_name).upper()))

        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 5.7 * inch, 'FECHA DE NACIMIENTO:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(1.5 * inch, 5.7 * inch,
                     '{}'.format(instancia.fecha_nacimiento.strftime("%d/%m/%Y")))

        p.setFont('Helvetica', 10)
        p.drawString(2.4 * inch, 5.7 * inch, 'SEXO:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(2.9 * inch, 5.7 * inch,
                     '{}'.format(str(instancia.sexo).upper()))

        p.setFont('Helvetica', 10)
        p.drawString(3.3 * inch, 5.7 * inch, 'EDAD:')
        resultado = datetime.date.today() - instancia.fecha_nacimiento

        p.setFont('Helvetica-Bold', 10)
        p.drawString(3.8 * inch, 5.7 * inch,
                     '{}'.format(int(resultado.days) // 365))

        p.setFont('Helvetica', 10)
        p.drawString(4.2 * inch, 5.7 * inch, 'CURP:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(4.7 * inch, 5.7 * inch,
                     '{}'.format(str(instancia.curp).upper()))

        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 5.4 * inch, 'DOMICILIO:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(0.6 * inch, 5.4 * inch,
                     '{}'.format(str(instancia.domicilio).upper()[:50]))

        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 5.1 * inch, 'COLONIA:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(0.5 * inch, 5.1 * inch,
                     '{}'.format(str(instancia.colonia).upper()))

        p.setFont('Helvetica', 10)
        p.drawString(4 * inch, 5.1 * inch, 'DELEGACIÓN:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(5 * inch, 5.1 * inch,
                     '{}'.format(str(instancia.delegacion).upper()))

        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 4.8 * inch, 'CÓDIGO POSTAL:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(1 * inch, 4.8 * inch,
                     '{}'.format(str(instancia.cp).upper()))

        p.setFont('Helvetica', 10)
        p.drawString(4 * inch, 4.8 * inch, 'TELÉFONO:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(4.85 * inch, 4.8 * inch,
                     '{}'.format(str(instancia.numero_casa).upper()))

        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 4.5 * inch, 'E-mail:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(0.3 * inch, 4.5 * inch,
                     '{}'.format(str(instancia.email)))

        p.setFont('Helvetica', 10)
        p.drawString(4 * inch, 4.5 * inch, 'TELÉFONO CELULAR:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(5.5 * inch, 4.5 * inch,
                     '{}'.format(str(instancia.numero_celular).upper()))


        #DATOS PADRE O TUTOR

        p.setFont('Helvetica-Bold', 11)
        p.drawCentredString(3.2 * inch, 4.1 * inch, 'DATOS DEL PADRE O TUTOR')

        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 3.7 * inch, 'NOMBRE:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(0.5 * inch, 3.7 * inch,
                     '{}'.format(str(instancia.nombre_tutor).upper()))

        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 3.4 * inch, 'OCUPACIÓN:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(0.75 * inch, 3.4 * inch,
                     '{}'.format(str(instancia.ocupacion_tutor).upper()))

        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 3.1 * inch, 'DOMICILIO DEL TRABAJO:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(1.6 * inch, 3.1 * inch,
                     '{}'.format(str(instancia.direccion_tutor).upper()[:50]))

        p.setFont('Helvetica', 10)
        p.drawString(-0.2 * inch, 2.8 * inch, 'TELÉFONO PARTICULAR:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(1.55 * inch, 2.8 * inch,
                     '{}'.format(str(instancia.numeroUno_tutor).upper()))

        p.setFont('Helvetica', 10)
        p.drawString(4 * inch, 2.8 * inch, 'TELÉFONO CELULAR:')
        p.setFont('Helvetica-Bold', 10)
        p.drawString(5.5 * inch, 2.8 * inch,
                     '{}'.format(str(instancia.numeroDos_tutor).upper()))


        # Firmas
        p.setFont('Helvetica-Bold', 10)
        p.drawString(0.5 * inch, 1.3 * inch, 'FIRMA DEL ALUMNO')

        p.setFont('Helvetica-Bold', 10)
        p.drawString(4.2 * inch, 1.3 * inch, 'FIRMA DEL PADRE Ó TUTOR')

        p.line(5, 110, 170, 110)
        p.line(290, 110, 455, 110)
        p.line(155, 15, 310, 15)

        p.drawCentredString(3.2 * inch, 0 * inch, 'REVISÓ')

        p.setFont('Helvetica', 8)
        p.drawString(-0.2 * inch, 0 * inch, 'C.C.P. CONTROL ESCOLAR')
        p.setFont('Helvetica-Bold', 9)
        p.drawString(-0.2 * inch, -0.2 * inch, 'FECHA: {}'.format(datetime.datetime.now().strftime("%d/%m/%Y %H:%M")))


        # Close canvas
        p.showPage()
        p.save()

        # Response
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    else:
        redirect(reverse_lazy('inicio'))


@login_required
def download_cita(request):
    instancia = User.objects.get(id=request.user.id)

    if instancia.paso_1 == True and instancia.paso_2 == True and instancia.paso_3 == True and instancia.paso_4 == False:
        instancia.paso_4 = True;
        instancia.save()

    if instancia.paso_1 == True and instancia.paso_2 == True and instancia.paso_3 == True and instancia.paso_4 == True:
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}-cita.pdf"'.format(str(instancia.username))
        buffer = BytesIO()
        #Config canvas
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        p.translate(inch,inch)
        p.setStrokeColorRGB(0, 0, 0)
        p.setFillColorRGB(0, 0, 0)

        #Draw canvas

        #Cabecera
        p.setFont('Helvetica-Bold', 11)
        p.drawCentredString(3.2 * inch, 9.5 * inch, 'CENTRO DE ESTUDIOS TECNOLÓGICOS INDUSTRIAL Y DE SERVICIOS No. 2')
        p.drawCentredString(3.2 * inch, 9.3 * inch, '“DAVID ALFARO SIQUEIROS”')
        p.setFont('Helvetica-Bold', 13)
        p.drawCentredString(3.2 * inch, 8 * inch, 'CITA DE ATENCIÓN EN VENTANILLA')
        p.drawCentredString(3.2 * inch, 7.8 * inch, ' DE CONTROL ESCOLAR')

        dgeti = ImageReader('{}/img/cetis2_pdf.png'.format(settings.STATICFILES_DIRS[0]))
        p.drawImage(dgeti, 5.5 * inch,8 * inch, width=68, height=74, mask=None)



        p.setFont('Helvetica-Bold', 11)
        p.drawString(-0.2 * inch, 7 * inch, 'LOS DATOS DE TU CITA SON:')

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 6.5 * inch, 'Trámite:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(0.4 * inch, 6.5 * inch, 'reinscripción')
        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 6.2 * inch, 'Fecha:')
        p.setFont('Helvetica-Bold', 11)
        locale.setlocale(locale.LC_TIME, '')
        resultado = instancia.fecha_cita

        t = timedelta(hours=5)
        resultado = resultado - t

        p.drawString(0.3 * inch, 6.2 * inch, '{}'.format(resultado.strftime("%d/%m/%Y")))
        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 5.9 * inch, 'Hora:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(0.2 * inch, 5.9 * inch, '{}'.format(resultado.strftime("%H:%M")))
        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 5.3 * inch, 'Acude el día y la hora indicada con los documentos siguientes:')

        p.rect(-0.4 * inch, 2.9 * inch, 7.3 * inch, 2 * inch, stroke=1, fill=0)



        p.drawString(-0.2 * inch, 4.6 * inch, '- Solicitud de reinscripción (2 tantos)')
        p.drawString(-0.2 * inch, 4.3 * inch, '- Cédula del alumno (2 tantos)')
        p.drawString(-0.2 * inch, 4 * inch, '- Carta compromiso')
        p.drawString(-0.2 * inch, 3.7 * inch, '- Certificado médico actualizado con tipo de sangre (original y copia)')
        p.drawString(-0.2 * inch, 3.4 * inch, '- Copia del recibo telefónico')
        p.drawString(-0.2 * inch, 3.1 * inch, '- Copia del comprobante de tu aportación sellado por Contraloría')

        p.setFont('Helvetica-Bold', 11)
        p.drawString(5.05 * inch, -0.2 * inch, '{}'.format(instancia.username))

        dgeti = ImageReader('{}/img/qr.png'.format(settings.STATICFILES_DIRS[0]))
        p.drawImage(dgeti, 4.7 * inch, -0 * inch, width=140, height=140, mask=None)

        p.line(-20, 495, 470, 495)


        # Close canvas
        p.showPage()
        p.save()

        # Response
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    else:
        redirect(reverse_lazy('inicio'))





@login_required
def download_cedula(request):
    instancia = User.objects.get(id=request.user.id)

    if instancia.paso_1 == True and instancia.paso_2 == True and instancia.paso_3 == True and instancia.paso_4 == False:
        instancia.paso_4 = True;
        instancia.save()

    if instancia.paso_1 == True and instancia.paso_2 == True and instancia.paso_3 == True and instancia.paso_4 == True:
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{}-cedula.pdf"'.format(str(instancia.username))
        buffer = BytesIO()
        #Config canvas
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        p.translate(inch,inch)
        p.setStrokeColorRGB(0, 0, 0)
        p.setFillColorRGB(0, 0, 0)

        #Draw canvas

        #Cabecera
        p.setFont('Helvetica-Bold', 13)
        p.drawCentredString(3.2 * inch, 8.5 * inch, 'CÉDULA DEL ALUMNO')


        #
        #dgeti = ImageReader('{}/{}'.format(settings.STATICFILES_DIRS[0], instancia.imagen_perfil))
        #p.drawImage(dgeti, 5.5 * inch,8 * inch, width=100, height=100, mask=None)
        #

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 7.5 * inch, 'NOMBRE DEL ALUMNO:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(1.6 * inch, 7.5 * inch, '{} {}'.format(str(instancia.first_name).upper(), str(instancia.last_name).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 7.2 * inch, 'CURP:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(0.4 * inch, 7.2 * inch,
                     '{} '.format(str(instancia.curp).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 6.9 * inch, 'GRUPO:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(0.45 * inch, 6.9 * inch,
                     '{} '.format(str(instancia.grupo).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(2.5 * inch, 6.9 * inch, 'ESPECIALIDAD:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(3.7 * inch, 6.9 * inch,
                     '{} '.format(str(instancia.carrera).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 6.6 * inch, 'TURNO:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(0.45 * inch, 6.6 * inch,
                     '{} '.format(str(instancia.turno).upper()))


        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 6.3 * inch, 'FECHA DE NACIMIENTO:')
        p.setFont('Helvetica-Bold', 11)
        locale.setlocale(locale.LC_TIME, '')
        p.drawString(1.67 * inch, 6.3 * inch,
                     '{} '.format(instancia.fecha_nacimiento.strftime("%d de %B de %Y").upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 6 * inch, '¿CUENTA CON ALGÚN SERVICIO MÉDICO?')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(3.05 * inch, 6 * inch,
                     '{} '.format(str(instancia.servicio_medico).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(3.4 * inch, 6 * inch, '¿CUÁL?')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(4.05 * inch, 6 * inch,
                     '{} '.format(str(instancia.des_servicio_medico).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 5.7 * inch, 'NÚMERO DE SEGURIDAD SOCIAL:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(2.4 * inch, 5.7 * inch,
                     '{} '.format(str(instancia.nss).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 5.4 * inch, 'DIRECCIÓN:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(0.75 * inch, 5.4 * inch,
                     '{} {} {} {}'.format(str(instancia.domicilio).upper(), str(instancia.colonia).upper(), str(instancia.delegacion).upper(), str(instancia.cp).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 5.1 * inch, 'TELÉFONO CASA:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(1.2 * inch, 5.1 * inch,
                     '{} '.format(str(instancia.numero_casa).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(3 * inch, 5.1 * inch, 'TELÉFONO CELULAR:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(4.67 * inch, 5.1 * inch,
                     '{} '.format(str(instancia.numero_casa).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 4.8 * inch, 'CORREO ELECTRÓNICO:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(1.7 * inch, 4.8 * inch,
                     '{} '.format(str(instancia.email).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 4.5 * inch, 'TIPO DE SANGRE:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(1.2 * inch, 4.5 * inch,
                     '{} '.format(str(instancia.tipo_sangre).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 4.2 * inch, 'ALERGIAS:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(0.65 * inch, 4.2 * inch,
                     '{} '.format(str(instancia.alergias).upper()[:50]))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 3.9 * inch, 'PADECIMIENTOS O ENFERMEDADES CRÓNICAS:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(3.45 * inch, 3.9 * inch,
                     '{} '.format(str(instancia.enf_cronicas).upper()[:50]))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 3.6 * inch, 'MEDICAMENTOS QUE TOMA DE MANERA PERMANENTE:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(4.04 * inch, 3.6 * inch,
                     '{} '.format(str(instancia.medicamentos).upper()[:50]))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 3.3 * inch, 'IMPEDIMENTOS:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(1.05 * inch, 3.3 * inch,
                     '{} '.format(str(instancia.impedimentos).upper()[:50]))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 3 * inch, 'EN CASO DE ACCIDENTE O MALESTAR INDICAR EL TELÉFONO Y NOMBRE DE LA PERSONA A')
        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 2.7 * inch,
                     'QUIEN AVISAR:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(1.05 * inch, 2.7 * inch,
                     '{} {}'.format(str(instancia.numeroUno_tutor).upper(), str(instancia.nombre_tutor).upper()))

        p.setFont('Helvetica-Bold', 12)
        p.drawCentredString(3.2 * inch, 2.25 * inch, 'DATOS DEL RESPONSABLE DEL ALUMNO (TUTOR)')

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 1.8 * inch, 'NOMBRE:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(0.6 * inch, 1.8 * inch,
                     '{} '.format(str(instancia.nombre_tutor).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 1.5 * inch, 'DIRECCIÓN:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(0.75 * inch, 1.5 * inch,
                     '{} '.format(str(instancia.direccion_tutor).upper()[:50]))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 1.2 * inch, 'OCUPACIÓN:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(0.81 * inch, 1.2 * inch,
                     '{} '.format(str(instancia.ocupacion_tutor).upper()[:50]))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 0.9 * inch, 'LUGAR DE TRABAJO:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(1.4 * inch, 0.9 * inch,
                     '{} '.format(str(instancia.trabajo_tutor).upper()[:50]))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 0.6 * inch, 'TELÉFONO DE CONTACTO 1:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(2 * inch, 0.6 * inch,
                     '{} '.format(str(instancia.numeroUno_tutor).upper()))

        p.setFont('Helvetica', 11)
        p.drawString(-0.2 * inch, 0.3 * inch, 'TELÉFONO DE CONTACTO 2:')
        p.setFont('Helvetica-Bold', 11)
        p.drawString(2 * inch, 0.3 * inch,
                     '{} '.format(str(instancia.numeroDos_tutor).upper()))

        # Close canvas
        p.showPage()
        p.save()

        # Response
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    else:
        redirect(reverse_lazy('inicio'))
