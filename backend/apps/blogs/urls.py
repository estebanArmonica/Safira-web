from django.urls import path
from . import views

urlBlogs = [
    path('news/', views.blog_safira, name='news'),
    path('news/pasos-para-pasar-de-un-cliente-regulado-a-ser-un-cliente-libre/', views.blog_migrar_libre, name='pasos-para-pasar-de-un-cliente-regulado-a-ser-un-cliente-libre'),
]