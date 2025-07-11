document.addEventListener('DOMContentLoaded', function () {
    const submitBtn = document.getElementById('submitButton');
    const contactForm = document.getElementById('contactForm');

    // Deshabilitar botón inicialmente
    submitBtn.disabled = true;

    // Habilitar botón cuando reCAPTCHA se complete
    function enableSubmit() {
        submitBtn.disabled = false;
        submitBtn.style.opacity = '1';
        submitBtn.style.cursor = 'pointer';
    }

    // Manejar envío del formulario
    contactForm.addEventListener('submit', function () {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Enviando...';
    });

    // Asignar la función al callback de reCAPTCHA
    window.onRecaptchaSuccess = function () {
        enableSubmit();
    };
});