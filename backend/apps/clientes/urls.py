from django.urls import path
from . import views

urlsClientes =[
    path('home/', views.principal, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
    path('cotizacion/', views.cotizacion, name='cotizacion'),
]