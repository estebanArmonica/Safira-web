from django.shortcuts import render

# Función de vista para la página principal
def principal(request):
    return render(request, 'base/principal.html')

def nosotros(request):
    return render(request, 'nosotros.html')

def contacto(request):
    return render(request, 'contacto.html')

def cotizacion(request):
    return render(request, 'cotizacion.html')

def mercado_libre(request):
    return render(request, 'mercado-libre.html')