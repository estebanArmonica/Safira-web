from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
import requests

# Función de vista para la página principal
def principal(request):
    return render(request, 'base/principal.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def contacto(request):
    if request.method == 'POST':
        
        # verificamos el reCAPTCHA
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
        
        if not result['success']:
            messages.error(request, 'Por favor, completa correctamente el reCAPTCHA.')
        else:
            messages.success(request, 'Mensaje enviado correctamente.')
            return render(request, 'contacto.html')
    return render(request, 'contacto.html')

def cotizacion(request):
    return render(request, 'cotizacion.html')

def mercado_libre(request):
    return render(request, 'mercado-libre.html')