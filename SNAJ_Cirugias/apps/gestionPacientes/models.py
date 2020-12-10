from django.db import models

# Create your models here.

from SNAJ_Cirugias.apps.utilidades.Choices import TiposID 

class Persona(models.Model):

    class Meta:
        db_table = 'Persona'

    idPersona = models.AutoField(primary_key=True)
    identificacion = models.CharField(max_length=15, unique=True)
    tipoIdentificacion = models.CharField(max_length=3,choices=TiposID.TIPOS_ID)
    fechaNacimiento = models.DateField()
    correo = models.EmailField(max_length = 50, null=True, blank=True)
    telefono = models.CharField(max_length=30)
    direccion = models.CharField(max_length=50)
    nombre = models.CharField(max_length=60)
    genero = models.CharField(max_length=15)

