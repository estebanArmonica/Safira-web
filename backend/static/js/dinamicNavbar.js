document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Remover la clase active de todos los enlaces
            navLinks.forEach(item => {
                item.classList.remove('active');
                item.classList.remove('show'); // Para dropdowns
            });
            
            // Agregar active al enlace clickeado
            this.classList.add('active');
            
            // Si es un dropdown, mantenerlo abierto
            if (this.classList.contains('dropdown-toggle')) {
                this.classList.add('show');
                const dropdownMenu = this.nextElementSibling;
                if (dropdownMenu) {
                    dropdownMenu.classList.add('show');
                }
            }
        });
    });
    
    // Cerrar offcanvas al hacer clic en un enlace (para móvil)
    const offcanvasLinks = document.querySelectorAll('.offcanvas-body .nav-link');
    const offcanvasInstance = bootstrap.Offcanvas.getInstance(document.getElementById('mobileMenu'));
    
    offcanvasLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (offcanvasInstance) {
                offcanvasInstance.hide();
            }
        });
    });
});