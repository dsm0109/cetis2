"""cetis_2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from cetis_2.apps.alumno import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^servicios-escolares/', admin.site.urls),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^logout/$', views.log_out, name='logout'),
    url(r'^$', views.inicio, name='inicio'),
    url(r'^mi-informacion/$', views.mi_info, name='mi_info'),
    url(r'^pago/$', views.pago, name='pago'),
    url(r'^reglamento/$', views.reglamento, name='reglamento'),
    url(r'^cita/$', views.cita, name='cita'),
    url(r'^mi-informacion/editar$', views.editar, name='editar'),

    url(r'^solicitud-inscripcion$', views.download_inscripcion, name='solicitud_inscripcion'),
    url(r'^download-cita$', views.download_cita, name='download_cita'),
    url(r'^download-cedula$', views.download_cedula, name='download_cedula'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

