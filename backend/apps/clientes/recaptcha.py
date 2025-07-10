import requests
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_recaptcha(token, ip=None):
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token
    }
    if ip:
        data['remoteip'] = ip
    
    response = requests.post(
        settings.RECAPTCHA_VERIFY_URL,
        data=data,
        timeout=5
    )
    
    result = response.json()
    
    if not result.get('success'):
        errors = result.get('error-codes', [])
        error_message = 'reCAPTCHA inválido. Por favor, inténtalo de nuevo.'
        
        if 'missing-input-secret' in errors:
            error_message = 'La clave secreta de reCAPTCHA no está configurada.'
        elif 'invalid-input-secret' in errors:
            error_message = 'La clave secreta de reCAPTCHA no es válida.'
        elif 'missing-input-response' in errors:
            error_message = 'Por favor, completa el reCAPTCHA.'
        elif 'invalid-input-response' in errors:
            error_message = 'La respuesta de reCAPTCHA no es válida.'
        elif 'timeout-or-duplicate' in errors:
            error_message = 'La respuesta de reCAPTCHA ha expirado. Por favor, inténtalo de nuevo.'
        
        raise ValidationError(error_message)
    
    return True