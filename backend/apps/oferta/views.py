import re
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import  redirect, render
from sweetify import sweetify
from ..services.arcgis_services import LocationIQGeocoder
from .models import Archivo, Comuna, Formulario, TipoCliente, Region
from .formOferta import FormularioCotizacion
from django.http import JsonResponse
from backend.settings import EMAIL_HOST_USER

import logging, PyPDF2
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
                        pdf_file.seek(0)
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        
                        # verifica que el PDF tiene páginas
                        if len(pdf_reader.pages) == 0:
                            raise Exception("PDF vacío o corrupto")
                        
                        text = ""
                        for page in pdf_reader.pages:
                            text += page.extract_text() or ""
                            
                        # Procesamos el texto extraido con los datos específicos
                        archivo_info = process_pdf_text(text)
                        
                        # Actualizamos los campos del formulario si se encontraron los datos especificados
                        if 'nom_emp' in archivo_info:
                            form.cleaned_data['nom_emp'] = archivo_info['nom_emp']
                        if 'direccion' in archivo_info:
                            form.cleaned_data['direccion'] = archivo_info['direccion']
                        if 'numero_cliente' in archivo_info and not cleaned_data.get('numero_cliente'):
                            cleaned_data['numero_cliente'] = archivo_info['numero_cliente']
                            
                    except Exception as e:
                        logger.error(f'Error al leer PDF: {str(e)}')
                
                comuna_obj = cleaned_data['comuna']
                region_nombre = comuna_obj.id_region.nom_region if hasattr(comuna_obj, 'id_region') else 'Región Metropolitana'
                
                # Geo codificamos la direccion del cliente
                geocoder = LocationIQGeocoder()
                
                # guardamos los datos del resultado de la geocodficación
                geocoder_result = geocoder.geocode_address(
                    address=cleaned_data['direccion_cli'],
                    region=region_nombre,
                    comuna=comuna_obj.nom_comuna
                )
                
                """
                    En caso de que no existe el resultado sobre la dirección se le mostrara un mensaje
                    al cliente, indicando el error del resultado y el campo que debe editar.
                """
                if not geocoder_result:
                    sweetify.error(
                        request,
                        'Error en la dirección',
                        text=f'No pudimos validar la dirección. Dirección: {cleaned_data["direccion_cli"]}',
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
                #geocoded_comuna = geocoder_result.get('comuna', '').lower()
                actual_comuna = comuna_obj.nom_comuna.lower()
                
                if geocoded_comuna and actual_comuna not in geocoded_comuna:
                    sweetify.warning(
                        request,
                        'Posible error en comuna',
                        text=f'La dirección parece corresponder a {geocoded_comuna.title()} en lugar de {actual_comuna.title()}',
                        button='OK'
                    )
                    return render(request, 'cotizacion.html', {'form': form})
                 
                # Obtener objeto TipoCliente
                tipo_cliente_obj = cleaned_data['tipo_cliente']
                 
                # creamos y guardamos la cotizacion (formulario)
                cotizacion = Formulario(
                    nom_person = cleaned_data['nom_person'],
                    nom_emp = cleaned_data['nom_emp'],
                    rut_emp = cleaned_data['rut_emp'],
                    correo = cleaned_data['correo'],
                    telefono = cleaned_data['telefono'],
                    direccion = cleaned_data['direccion'],
                    direccion_cli = cleaned_data['direccion_cli'],
                    id_distrib = cleaned_data['distribuidora'],
                    id_comuna = comuna_obj,
                    consum_elect = cleaned_data['consum_elect'],
                    demanda_max = cleaned_data['demanda_max'],
                    demanda_max_hp = cleaned_data['demanda_max_hp'],
                    subestacion = cleaned_data['subestacion'],
                    tarif_contratada = cleaned_data['tarif_contratada'],
                    id_tip_cliente = tipo_cliente_obj,
                    ubicacion = f"POINT({geocoder_result['longitude']} {geocoder_result['latitude']})",
                    numero_cliente=cleaned_data.get('numero_cliente', ''),
                )
                
                # rescatamos los datos y los guardamos 
                cotizacion.save()
                
                # Guardar archivo en la base de datos
                if file_name:
                    # Determinar tipo de documento basado en el nombre del archivo
                    if 'factura' in pdf_file.name.lower():
                        tipo_documento = 'Factura'
                    elif 'boleta' in pdf_file.name.lower():
                        tipo_documento = 'Boleta'
                    else:
                        tipo_documento = 'PDF'
                    
                    archivo = Archivo(
                        url_archivo=file_name,
                        nombre_archivo=pdf_file.name,
                        tipo=tipo_documento,
                        id_form=cotizacion
                    )
                    archivo.save()
                    
                # creamos el formato del correo una véz este listo la solicitud de la cotización
                asunto = 'Solicitud de Cotización recibida por Safira Energía Chile'
                mensaje = f"""
                    Hola {cleaned_data["nom_person"]},

                    Hemos recibido de forma exitosa tu solicitud de cotización con los siguientes datos:
                    
                    Nombre: {cleaned_data['nom_person']}
                    Empresa: {cleaned_data['nom_emp']}
                    RUT Empresa: {cleaned_data['rut_emp']}
                    Correo: {cleaned_data['correo']}
                    Teléfono: {cleaned_data['telefono']}
                    Dirección Suministro: {cleaned_data['direccion']}
                    Su dirección: {cleaned_data['direccion_cli']}
                    Región: {region_nombre}
                    Comuna: {comuna_obj.nom_comuna}
                    Tipo de Cliente: {tipo_cliente_obj.nom_tip_cli}
                    Distribuidora: {cleaned_data.get('distribuidora', 'No especificada')}
                    Consumo Eléctrico: {cleaned_data['consum_elect']} kWh
                    Demanda Máxima: {cleaned_data['demanda_max']} kWh
                    Demanda Máxima HP: {cleaned_data['demanda_max_hp']} kWh
                    
                    Subestacion: {cleaned_data['subestacion']}
                    Tarifa actual: {cleaned_data['tarif_contratada']}
                    
                    Pronto nos pondremos en contacto contigo.

                    Saludos,
                    Safira Energía Chile
                """
                
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
        
    # nos aseguramos que siempre retorne una respuesta
    return render(request, 'cotizacion.html', {'form': form})
#=======================================================================================================================================================


# Añade esta función si no existe
def process_pdf_text(text):
    """
    Función para procesar texto extraído de PDF y extraer información específica
    Modifica según tus necesidades específicas
    """
    result = {}
    
    # Ejemplo de extracción básica - ajusta según tu formato de PDF
    try:
        # Extraer nombre de empresa
        empresa_match = re.search(r'Sr\.?\(?a\)?[:\s-]*(.+?)(?:\n|Dirección|$)', text, re.IGNORECASE)
        if empresa_match:
            result['nom_emp'] = empresa_match.group(1).strip()
        
        # Extraer dirección
        direccion_match = re.search(r'Direcci[óo]n suministro\s*[:\-]?\s*([^\n]+)', text, re.IGNORECASE)
        if direccion_match:
            result['direccion'] = direccion_match.group(1).strip()
        
        # Extraer número de cliente
        cliente_match = re.search(r'N[º°]?[\s-]*Cliente[\s:]*(\d{7,8}-\d)', text, re.IGNORECASE)
        if cliente_match:
            result['numero_cliente'] = cliente_match.group(1)
            
    except Exception as e:
        logger.error(f'Error procesando texto PDF: {str(e)}')
    
    return result
#=======================================================================================================================================================

# funcion que cargara todos las comunas dependiendo de la region escogida
def cargar_comunas(request):
    if request.method == 'POST':
        region_id = request.POST.get('id_region')
        comunas = Comuna.objects.filter(id_region=region_id).order_by('nom_comuna')
        return JsonResponse(list(comunas.values('id_comuna', 'nom_comuna')), safe=False)