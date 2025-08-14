// Filtrado por categoría
document.querySelectorAll('.category-filter').forEach(filter => {
    filter.addEventListener('click', function () {
        // Quitar clase active de todos los filtros
        document.querySelectorAll('.category-filter').forEach(f => {
            f.classList.remove('active');
        });

        // Añadir clase active al filtro clickeado
        this.classList.add('active');

        const category = this.dataset.category;
        const blogCards = document.querySelectorAll('.blog-card');

        // Mostrar/ocultar artículos según categoría
        blogCards.forEach(card => {
            if (category === 'all' || card.dataset.category === category) {
                card.style.display = 'block';
                setTimeout(() => {
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 50);
            } else {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    card.style.display = 'none';
                }, 300);
            }
        });
    });
});

// Simulación de carga más artículos
document.querySelector('.load-more-button').addEventListener('click', function () {
    this.disabled = true;
    this.innerHTML = 'Cargando... <i class="fas fa-spinner fa-spin"></i>';

    // Simular carga AJAX
    setTimeout(() => {
        // Aquí iría la lógica para cargar más artículos
        alert('Se cargarían más artículos en una implementación real');
        this.disabled = false;
        this.innerHTML = 'Cargar más artículos <i class="fas fa-sync-alt"></i>';
    }, 1500);
});

// Animación de aparición al hacer scroll
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.blog-card').forEach(card => {
    observer.observe(card);
});