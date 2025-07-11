from pydoc import text
from django.shortcuts import render
from backend.settings import EMAIL_HOST_USER, RECAPTCHA_SECRET_KEY
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from sweetify import sweetify
import requests, logging

from .formContacto import FormularioContacto

logger = logging.getLogger(__name__)

# Función de vista para la página principal
def principal(request):
    return render(request, 'base/principal.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def contacto(request):
    # creamos la instancia del formulario
    form = FormularioContacto()
    
    if request.method == 'GET':
        contexto = {
            'form': form
        }
        return render(request, 'contacto.html', contexto)
    
    if request.method == 'POST':
        form = FormularioContacto(data=request.POST)
        
        # verificamos el reCAPTCHA
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        if not recaptcha_response:
            sweetify.error(request, 'Error!\n, Por favor, completa el reCAPTCHA.', button='OK')
            return render(request, 'contacto.html', {'form': form})
        
        try:
            # validamos el reCAPTCHA con la API de Google
            data = {
                'secret': RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            
            url = f'https://www.google.com/recaptcha/api/siteverify'
            
            r = requests.post(url, data=data)
            result = r.json()
            
            if not result.get('success'):
                sweetify.error(request, 'Error!\nPor favor, completa correctamente el reCAPTCHA.', button='OK')
                return render(request, 'contacto.html', {'form': form})
        
            # si el formulario es válido
            if form.is_valid():
                # Procesar datos del formulario
                nombre = request.POST.get('nombre')
                email = request.POST.get('email')
                asunto = request.POST.get('asunto')
                mensaje = request.POST.get('mensaje')
                
                # Envíamos el correo
                email_body = f"""
                    Nombre: {nombre}
                    Email: {email}
                    Asunto: {asunto}
                    Mensaje: 
                    {mensaje}
                """
                
                try:
                    # creamos el EmailMessage
                    email_msg = EmailMessage(
                        subject=asunto,
                        body=email_body,
                        from_email=f'{nombre} <{email}>',
                        to=[EMAIL_HOST_USER],
                        reply_to=[email]
                    )
                    
                    email_msg.send()
                    
                    sweetify.success(request, '¡Mensaje enviado con éxito!\n, Te responderemos pronto.', button='Cerrar')
                    return redirect('contactos')
                except Exception as e:
                    logger.error(f'Error al enviar el mensaje de contacto: {str(e)}')
                    sweetify.error(request, 'Error\nOcurrió un error al enviar el mensaje. Por favor, inténtalo de nuevo más tarde.', button='Entendido')
        except requests.RequestException as e:
            logger.error(f'Error al verificar reCAPTCHA: {str(e)}')
            sweetify.error(request,'Error al verificar el reCAPTCHA. Por favor inténtalo de nuevo.')    
    return render(request, 'contacto.html', {'form': form})

def cotizacion(request):
    return render(request, 'cotizacion.html')

def mercado_libre(request):
    return render(request, 'mercado-libre.html')