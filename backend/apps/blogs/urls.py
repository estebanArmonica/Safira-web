from django.urls import path
from . import views

urlBlogs = [
    path('news/', views.blog_safira, name='news'),
    path('news/pasos-para-pasar-de-un-cliente-regulado-a-ser-un-cliente-libre/', views.blog_migrar_libre, name='pasos-para-pasar-de-un-cliente-regulado-a-ser-un-cliente-libre'),
    path('news/como-la-transformación-digital-ha-sido-una-de-las-principales-preocupaciones-en-el-sector-eléctrico/', views.blog_transformacion_digital, name='como-la-transformación-digital-ha-sido-una-de-las-principales-preocupaciones-en-el-sector-eléctrico'),
    path('news/10-estrategias-comprobadas-para-reducir-tu-consumo-energético/', views.blog_estrategia, name='estrategias-comprobadas'),
    path('news/como-negociar-el-mejor-contrato-en-el-mercado-libre/', views.blog_negociar_contrato_safira, name='negociar-contrato'),
    path('news/tendencias-en-tecnologia-verde-que-transformaran-el-2025/', views.blog_tendencia_tecnologica_safira, name='tendencia-tecnologica'),
]