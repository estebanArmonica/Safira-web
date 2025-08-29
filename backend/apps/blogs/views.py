from django.shortcuts import render

# sobre bolg de la empresa
def blog_safira(request):
    return render(request, 'blog/blog-safira.html')

def blog_migrar_libre(request):
    return render(request, 'blog/migrar-libre.html')

def blog_transformacion_digital(request):
    return render(request, 'blog/transformacion-digital.html')