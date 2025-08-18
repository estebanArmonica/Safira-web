import re
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import  redirect, render
from sweetify import sweetify
from ..services.arcgis_services import LocationIQGeocoder
from .models import Archivo, Comuna, Formulario, TipoCliente
from .formOferta import FormularioCotizacion
from django.http import JsonResponse
from backend.settings import EMAIL_HOST_USER
from reportlab.pdfgen import canvas

import logging, folium, imgkit, PyPDF2, io
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

# funcion para crear cotizaciones a los clientes nuevos de safira
def realizarCotizacion(request):
    return render(request, 'cotizacion.html')
#=======================================================================================================================================================

# funcion que cargara todos las comunas dependiendo de la region escogida
def cargar_comunas(request):
    if request.method == 'POST':
        region_id = request.POST.get('id_region')
        comunas = Comuna.objects.filter(id_region=region_id).order_by('nom_comuna')
        return JsonResponse(list(comunas.values('id_comuna', 'nom_comuna')), safe=False)