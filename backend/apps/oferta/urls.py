from django.urls import path
from . import views

urlCotizacion = [
    path('cotizacion/', views.realizarCotizacion, name='cotizaciones'),
]