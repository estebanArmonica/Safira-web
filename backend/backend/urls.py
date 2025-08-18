from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.clientes.urls import urlsClientes
from apps.oferta.urls import urlCotizacion
from apps.blogs.urls import urlBlogs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(urlsClientes)),
    path('crea-coti-safira/', include(urlCotizacion)),
    path('blogs-safira/', include(urlBlogs)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
