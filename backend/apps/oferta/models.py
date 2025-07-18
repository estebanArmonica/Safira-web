from django.db import models
from mapbox_location_field.models import LocationField

# Create your models here.
class Region(models.Model):
    nom_region = models.CharField(max_length=100)
    sigla = models.CharField(max_length=15)
    
    class Meta:
        verbose_name = 'region'
        verbose_name_plural = 'regiones'
        ordering = ('nom_region',)
        
    def __str__(self):
        return self.nom_region
    
class Comuna(models.Model):
    nom_comuna = models.CharField(max_length=60)
    ubicacion = LocationField()    
    id_region = models.ForeignKey(Region, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'comuna'
        verbose_name_plural = 'comunas'
        ordering = ('nom_comuna',)
        
    def __str__(self):
        return self.nom_comuna
    
class Distribuidora(models.Model):
    razon_social = models.CharField(max_length=55)
    nombre_fantasia = models.CharField(max_length=55)
    
    class Meta:
        verbose_name = 'distribuidora'
        verbose_name_plural = 'distribuidoras'
        ordering = ('nombre_fantasia',)
        
    def __str__(self):
        return self.nombre_fantasia
    
class TipoCliente(models.Model):
    nom_tip_cli = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = 'tipo_cliente'
        verbose_name_plural = 'tipo_clientes'
        ordering = ('nom_tip_cli',)
        
    def __str__(self):
        return self.nom_tip_cli
    
class Cotizacion(models.Model):
    nom_person = models.CharField(max_length=50)
    nom_emp = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    telefono = models.IntegerField()
    direccion = models.CharField(max_length=255)
    id_distrib = models.ForeignKey(Distribuidora, on_delete=models.CASCADE)
    id_comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)
    id_tip_cliente = models.ForeignKey(TipoCliente, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'formulario'
        verbose_name_plural = 'formularios'
        ordering = ('correo',)
        
    def __str__(self):
        return self.correo