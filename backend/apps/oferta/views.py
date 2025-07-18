from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import  redirect, render
from sweetify import sweetify
import requests, logging

from .models import Comuna, Cotizacion
from .formOferta import FormularioCotizacion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

# funcion para crear cotizaciones a los clientes nuevos de safira
def realizarCotizacion(request):
    
    # instancioa del formulario para generar la oferta a cliente
    formularioOferta = FormularioCotizacion()
    logger.info(f'Formulario instanciado correctamente: {formularioOferta}')
    
    if request.method == 'GET':
        contexto = {
            'formularioOferta': formularioOferta
        }
        
        logger.info(f'Campos del formulario: {contexto}')
        print(f'Campos del formulario: {contexto}')
        return render(request, 'cotizacion.html', contexto)
    
    if request.method == 'POST':
        formularioOferta = FormularioCotizacion(data=request.POST)
        
        if formularioOferta.is_valid():
            try:
                # Obtenemos los datos del formulario
                logger.info('formulario valido')
                
                # Crear y guardar la cotización en la base de datos
                cotizacion = Cotizacion(
                    nom_person = request.POST.get('nom_person'),
                    nom_emp = request.POST.get('nom_emp'),
                    correo = request.POST.get('correo'),
                    telefono = request.POST.get('telefono'),
                    region = request.POST.get('region'),
                    comuna = request.POST.get('comuna'),
                    tipo_cliente = request.POST.get('tipo_cliente'),
                    distribuidora = request.POST.get('distribuidora'),
                    direccion = request.POST.get('direccion')
                )
                
                # Debug: mostramos los valores obtenidos
                print(f"Datos obtenidos con POST.get(): {request.POST}")
                logger.info(f"Datos para guardar: {cotizacion.__dict__}")
                
                cotizacion.save()
                
                sweetify.success(
                    request,
                    'Cotización enviada correctamente',
                    text='Nos pondremos en contacto contigo pronto',
                    button='OK'
                )
                return redirect('cotizaciones')
                
            except requests.RequestException as e:
                logger.error(f'Error al guardar cotizacion: {str(e)}')
                sweetify.error(
                    request,
                    'Error al procesar tu solicitud',
                    text='Por favor intenta nuevamente más tarde',
                    button='OK'
                )
                return render(request, 'cotizacion.html', {'formularioOferta': formularioOferta})
        else:
            sweetify.error(
                request,
                'Error en el formulario',
                text='Por favor corriga los errores marcados',
                button='OK'
            )
            return render(request, 'cotizacion.html', {'formularioOferta': formularioOferta})
#=======================================================================================================================================================

# funcion que cargara todos las comunas dependiendo de la region escogida
@csrf_exempt
def cargar_comunas(request):
    if request.method == 'POST':
        region_id = request.POST.get('id_region')
        comunas = Comuna.objects.filter(id_region=region_id).order_by('nom_comuna')
        return JsonResponse(list(comunas.values('id_comuna', 'nom_comuna')), safe=False)