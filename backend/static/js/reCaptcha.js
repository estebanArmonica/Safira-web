document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('contactForm');
    const submitButton = document.getElementById('submitButton');
    const recaptchaError = document.getElementById('recaptcha-error');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        // Resetear mensajes de error
        recaptchaError.style.display = 'none';
        
        // Deshabilitar botón y mostrar estado de carga
        submitButton.disabled = true;
        submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Enviando...';
        
        // Validar reCAPTCHA
        const recaptchaResponse = grecaptcha.getResponse();
        if (!recaptchaResponse) {
            recaptchaError.style.display = 'block';
            recaptchaError.textContent = 'Por favor, completa el reCAPTCHA';
            submitButton.disabled = false;
            submitButton.innerHTML = 'Enviar Mensaje';
            
            // Scroll suave al error
            recaptchaError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return;
        }
        
        try {
            // Crear FormData y añadir todos los campos
            const formData = new FormData(form);
            formData.append('g-recaptcha-response', recaptchaResponse);
            
            // Enviar datos al servidor
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': '{{ csrf_token }}'
                }
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Error en la respuesta del servidor');
            }
            
            if (data.success) {
                // Mostrar mensaje de éxito (puedes usar un modal o toast en lugar de alert)
                showAlert('success', 'Mensaje enviado correctamente');
                form.reset();
                grecaptcha.reset();
            } else {
                // Manejar errores específicos de reCAPTCHA
                if (data.recaptcha_error) {
                    recaptchaError.style.display = 'block';
                    recaptchaError.textContent = data.recaptcha_error;
                    recaptchaError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
                showAlert('error', data.error || 'Error al enviar el formulario');
            }
        } catch (error) {
            console.error('Error:', error);
            showAlert('error', 'Ocurrió un error al enviar el formulario: ' + error.message);
        } finally {
            submitButton.disabled = false;
            submitButton.innerHTML = 'Enviar Mensaje';
        }
    });
    
    // Función para mostrar alertas (puedes personalizar esto)
    function showAlert(type, message) {
        // Aquí puedes implementar un sistema de notificaciones más elegante
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} fixed-top mt-3 mx-auto w-75`;
        alertDiv.style.zIndex = '1050';
        alertDiv.textContent = message;
        
        document.body.appendChild(alertDiv);
        
        setTimeout(() => {
            alertDiv.classList.add('fade');
            setTimeout(() => alertDiv.remove(), 300);
        }, 5000);
    }
});