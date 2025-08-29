from django.urls import path
from . import views

urlBlogs = [
    path('news/', views.blog_safira, name='news'),
    path('news/pasos-para-pasar-de-un-cliente-regulado-a-ser-un-cliente-libre/', views.blog_migrar_libre, name='pasos-para-pasar-de-un-cliente-regulado-a-ser-un-cliente-libre'),
    path('news/como-la-transformación-digital-ha-sido-una-de-las-principales-preocupaciones-en-el-sector-eléctrico/', views.blog_transformacion_digital, name='como-la-transformación-digital-ha-sido-una-de-las-principales-preocupaciones-en-el-sector-eléctrico'),
]