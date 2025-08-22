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
    # realizamos un GET para mostrar el formulario
    if request.method == 'GET':
        
        # creamos la instancia del formulario
        form = FormularioCotizacion()
        contexto = {'form': form}
        return render(request, 'cotizacion.html', contexto)
    
    
    # realizamos un POST para crear la logica y agregar los datos que se vayan guardando por el formulario
    if request.method == 'POST':
        form = FormularioCotizacion(request.POST, request.FILES)
        
        # validamos si el formulario existe
        if form.is_valid():
            # crealizamos un try-exceptions para manejo de errores
            try:
                # obtenemos los datos del formulario
                cleaned_data = form.cleaned_data
                
                archivo_info = {} # creamos una arreglo vacia
                file_name = None # como no sabemos el nombre creamos una variable vacia "osea tipo None"
                
                # Extraermos la información del PDF (Boleta o Factura)
                if 'archivo' in request.FILES:
                    pdf_file = request.FILES['archivo']
                    file_name = default_storage.save(f'archivos/{pdf_file.name}', ContentFile(pdf_file.read()))
                    
                    # Extraemos la información del PDF
                    try:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text()
                            
                        # Procesamos el texto extraido con los datos específicos
                        archivo_info = process_pdf_text(text)
                        
                        # Actualizamos los campos del formulario si se encontraron los datos especificados
                        if 'nom_emp' in archivo_info:
                            form.cleaned_data['nom_emp'] = archivo_info['nom_emp']
                        if 'direccion' in archivo_info:
                            form.cleaned_data['direccion'] = archivo_info['direccion']
                    except Exception as e:
                        logger.error(f'Error al leer PDF: {str(e)}')
                
                # geocodificamos la dirección
                geocoder = LocationIQGeocoder()
                region = cleaned_data['region'].nom_region
                comuna = cleaned_data['comuna'].nom_comuna
                
                # guardamos los datos del resultado de la geocodficación
                geocoder_result = geocoder.geocode_address(
                    address=cleaned_data['direccion'],
                    region='Región Metropolitana',
                    comuna=comuna
                )
                
                """
                    En caso de que no existe el resultado sobre la dirección se le mostrara un mensaje
                    al cliente, indicando el error del resultado y el campo que debe editar.
                """
                if not geocoder_result:
                    sweetify.error(
                        request,
                        'Error en la dirección',
                        text=f'No pudimos validar la dirección. Dirección: {cleaned_data["direccion"]}',
                        button='OK'
                    )
                    return render(request, 'cotizacion.html', {'form': form})
                
                # Validamos que la comuna sea la correspondiente y escogida por el cliente
                address = geocoder_result.get('address_details', {})
                geocoded_comuna = (
                    address.get('city') or
                    address.get('town') or
                    address.get('municipality') or
                    address.get('village') or
                    address.get('suburb') or
                    address.get('neighbourhood') or
                    ''
                ).lower()   
                
                # Verificamos coincidencias con comunas seleccionadas
                geocoded_comuna = geocoder_result.get('comuna', '').lower()
                
                if geocoded_comuna and comuna.lower() not in geocoded_comuna:
                    sweetify.warning(
                        request,
                        'Posible error en comuna',
                        text=f'La dirección parece corresponder a {geocoded_comuna.title()} en lugar de {comuna}',
                        button='OK'
                    )
                    return render(request, 'cotizacion.html', {'form': form})
                 
                # creamos y guardamos la cotizacion (formulario)
                cotizacion = Formulario(
                    nom_person = cleaned_data['nom_person'],
                    nom_emp = cleaned_data['nom_emp'],
                    rut_emp = cleaned_data['rut_emp'],
                    correo = cleaned_data['correo'],
                    telefono = cleaned_data['telefono'],
                    direccion = cleaned_data['direccion'],
                    id_distrib = cleaned_data['distribuidora'],
                    id_comuna = cleaned_data['comuna'],
                    consum_elect = cleaned_data['consum_elect'],
                    demanda_max = cleaned_data['demanda_max'],
                    demanda_max_hp = cleaned_data['demanda_max_hp'],
                    id_tip_cliente = TipoCliente.objects.get(nom_tip_cli = cleaned_data['tipo_cliente']),
                    ubicacion = f"POINT({geocoder_result['longitude']} {geocoder_result['latitude']})",
                    numero_cliente=cleaned_data['numero_cliente'],
                    #numero_cliente=archivo_info.get('numero_cliente', ''),
                )
                
                # rescatamos los datos y los guardamos 
                cotizacion.save()
                
                # rescatamos el archivo si existe
                if file_name:
                    archivo = Archivo(
                        url_archivo=file_name,
                        nombre_archivo=pdf_file.name,
                        tipo=archivo_info.get('tipo_documento', 'PDF'),
                        id_form=cotizacion
                    )
                    archivo.save()
                    
                # creamos el formato del correo una véz este listo la solicitud de la cotización
                asunto = 'Solicitud de Cotización recibida por Safira Energía Chile'
                mensaje = (
                    f'Hola {cleaned_data["nom_person"]},\n\n'
                    f'Hemos recibido de forma exitosa tu solicitud de cotización con los siguientes datos:\n'
                    f"Nombre: {cleaned_data['nom_person']}\n"
                    f"Empresa: {cleaned_data['nom_emp']}\n"
                    f"Correo: {cleaned_data['correo']}\n"
                    f"Teléfono: {cleaned_data['telefono']}\n"
                    f"Dirección: {cleaned_data['direccion']}\n"
                    f"Región: {region}\n"
                    f"Comuna: {comuna}\n"
                    f"Tipo de Cliente: {cleaned_data['tipo_cliente']}\n"
                    f"Distribuidora: {cleaned_data['distribuidora']}\n"
                    f"Tipo de Solicitud: {cleaned_data['tipo_solicitud']}\n"
                    '\nPronto nos pondremos en contacto contigo.\n\nSaludos,\nSafira Energía Chile'
                )
                
                # correos destinados
                to_email = [cleaned_data['correo']]
                cc_email = [EMAIL_HOST_USER]
                
                email = EmailMessage(
                    subject=asunto,
                    body=mensaje,
                    from_email=EMAIL_HOST_USER,
                    to=to_email,
                    bcc=cc_email
                )
                
                email.send(fail_silently=False)
                
                # mostramos el mensaje de exito
                sweetify.success(
                    request,
                    'Cotización enviada',
                    text='Nos pondremos en contacto contigo pronto',
                    button='OK'
                )
                return redirect('cotizaciones')
            except Exception as e:
                logger.error(f'Error al guardar cotización: {str(e)}')
                print(f'Error al guardar cotización: {str(e)}')
                sweetify.error(
                    request,
                    'Error al procesar tu solicitud',
                    text='Por favor intenta nuevamente más tarde',
                    button='OK'
                )
                return render(request, 'cotizacion.html', {'form': form})
        else:
            sweetify.error(
                request,
                'Error en el formulario',
                text='Por favor corriga los errores marcados',
                button='OK'
            )
            return render(request, 'cotizacion.html', {'form': form})
#=======================================================================================================================================================
# procesamos el archivo pdf para ser convertido en texto
def process_pdf_text(text):
    result = {}
    
    # Patrones mejorados para extracción de datos
    nombre_empresa_match = re.search(r'(?:Señor\(es\)|Sr\.?\s?\(?a\)?):?\s*([^\n]+)', text, re.IGNORECASE)
    if nombre_empresa_match:
        result['nom_emp'] = nombre_empresa_match.group(1).strip()
    
    direccion_match = re.search(r'Dirección(?: suministro)?\s*:\s*([^\n]+)', text, re.IGNORECASE) or \
                     re.search(r'Dirección(?: suministro)?\s*([^\n]+)', text, re.IGNORECASE)
    if direccion_match:
        result['direccion'] = direccion_match.group(1).strip()
    
    rut_match = re.search(r'(?:R\.U\.T\.|RUT)\s*:\s*([\d\.\-]+)', text, re.IGNORECASE)
    if rut_match:
        result['rut_empresa'] = rut_match.group(1).strip()
    
    cliente_match = re.search(r'N(?:ú|u)mero de cliente\s*:\s*([\d\-]+)', text, re.IGNORECASE)
    if cliente_match:
        result['numero_cliente'] = cliente_match.group(1).strip()
    
    return result

#=======================================================================================================================================================

# funcion que cargara todos las comunas dependiendo de la region escogida
def cargar_comunas(request):
    if request.method == 'POST':
        region_id = request.POST.get('id_region')
        comunas = Comuna.objects.filter(id_region=region_id).order_by('nom_comuna')
        return JsonResponse(list(comunas.values('id_comuna', 'nom_comuna')), safe=False)