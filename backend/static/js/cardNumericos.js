// Animación de contadores
document.addEventListener('DOMContentLoaded', function () {
    const counters = document.querySelectorAll('.counter');
    const speed = 200;

    function animateCounters() {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText;
            const increment = target / speed;
            const showPlus = counter.getAttribute('data-plus') === 'true';
            const plusIcon = counter.previousElementSibling;

            if (count < target) {
                const newCount = Math.ceil(count + increment);
                counter.innerText = newCount.toLocaleString();

                // Mostrar el icono + cuando el conteo comienza
                if (showPlus && plusIcon && count > 0) {
                    plusIcon.style.opacity = '1';
                }

                setTimeout(animateCounters, 1);
            } else {
                counter.innerText = target.toLocaleString();
                // Asegurarse de que el icono + permanezca visible al final
                if (showPlus && plusIcon) {
                    plusIcon.style.opacity = '1';
                }
            }
        });
    }

    // Activar cuando el elemento sea visible
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => {
        observer.observe(counter.parentElement.parentElement.parentElement);
    });
});