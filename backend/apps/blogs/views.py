from django.shortcuts import render

# sobre bolg de la empresa
def blog_safira(request):
    return render(request, 'blog/blog-safira.html')