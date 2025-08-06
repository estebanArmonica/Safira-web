function initMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const mobileMenu = document.getElementById('mobileMenu');
    
    if (!navbarToggler || !mobileMenu) return;
    
    try {
        const offcanvas = new bootstrap.Offcanvas(mobileMenu);
        
        // 1. Comportamiento del botón hamburguesa (se mantiene igual)
        navbarToggler.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            isExpanded ? offcanvas.show() : offcanvas.hide();
        });
        
        // 2. Configuración especial para el dropdown móvil (NUEVO)
        const mobileDropdown = document.getElementById('mobileDropdown');
        if (mobileDropdown) {
            // Evitar que el offcanvas se cierre al hacer clic en el dropdown
            mobileDropdown.addEventListener('click', function(e) {
                e.stopPropagation();
            });
            
            // Evitar cierre al interactuar con el menú desplegable
            const dropdownMenu = mobileMenu.querySelector('.dropdown-menu');
            if (dropdownMenu) {
                dropdownMenu.addEventListener('click', function(e) {
                    e.stopPropagation();
                });
            }
        }
        
        // 3. Cerrar offcanvas solo para enlaces normales (MODIFICADO)
        mobileMenu.querySelectorAll('.nav-link:not(.dropdown-toggle)').forEach(link => {
            link.addEventListener('click', () => offcanvas.hide());
        });
        
    } catch (error) {
        console.error('Error al inicializar el menú móvil:', error);
    }
}

// Inicialización (se mantiene igual)
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileMenu);
} else {
    initMobileMenu();
}