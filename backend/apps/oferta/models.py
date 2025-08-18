from django.db import models

class Region(models.Model):
    id_region = models.AutoField(primary_key=True)
    nom_region = models.CharField(max_length=100)
    sigla = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.nom_region}'

    class Meta:
        managed = False
        db_table = 'region'


class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nom_comuna = models.CharField(max_length=60)
    ubicacion = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_region = models.ForeignKey(Region, models.DO_NOTHING, db_column='id_region')

    def __str__(self):
        return f'{self.nom_comuna}'

    class Meta:
        managed = False
        db_table = 'comuna'


class Distribuidora(models.Model):
    id_distrib = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=55)
    nombre_fantasia = models.CharField(max_length=55)

    def __str__(self):
        return f'{self.nombre_fantasia}'

    class Meta:
        managed = False
        db_table = 'distribuidora'


class TipoCliente(models.Model):
    id_tip_cliente = models.AutoField(primary_key=True)
    nom_tip_cli = models.CharField(max_length=20)
    descripcion = models.TextField()

    def __str__(self):
        return f'{self.nom_tip_cli}'

    class Meta:
        managed = False
        db_table = 'tipo_cliente'


class Formulario(models.Model):
    id_form = models.AutoField(primary_key=True)
    nom_person = models.CharField(max_length=50)
    nom_emp = models.CharField(max_length=100)
    rut_emp = models.CharField(max_length=12)
    correo = models.CharField(max_length=60)
    telefono = models.DecimalField(max_digits=65535, decimal_places=65535)
    direccion = models.TextField()
    ubicacion = models.TextField(blank=True, null=True)
    consum_elect = models.DecimalField(max_digits=65535, decimal_places=65535)
    demanda_max = models.DecimalField(max_digits=65535, decimal_places=65535)
    demanda_max_hp = models.DecimalField(max_digits=65535, decimal_places=65535)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    numero_cliente = models.CharField(max_length=20, blank=True, null=True)
    id_distrib = models.ForeignKey(Distribuidora, models.DO_NOTHING, db_column='id_distrib', blank=True, null=True)
    id_comuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='id_comuna')
    id_tip_cliente = models.ForeignKey(TipoCliente, models.DO_NOTHING, db_column='id_tip_cliente')

    def __str__(self):
        return f'{self.id_form} - {self.nom_person} - {self.nom_emp} - {self.correo} - {self.telefono} - {self.direccion} - {self.id_distrib} - {self.id_comuna} - {self.id_tip_cliente} - {self.ubicacion}'

    class Meta:
        managed = False
        db_table = 'formulario'

class Archivo(models.Model):
    id_archivo = models.AutoField(primary_key=True)
    url_archivo = models.CharField(max_length=255)
    nombre_archivo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=25)
    id_form = models.ForeignKey(Formulario, models.DO_NOTHING, db_column='id_form')

    def __str__(self):
        return f"{self.id_archivo} - {self.nombre_archivo} - {self.tipo}"

    class Meta:
        managed = False
        db_table = 'archivo'