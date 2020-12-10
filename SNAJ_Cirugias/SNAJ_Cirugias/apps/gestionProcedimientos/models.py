from django.db import models

# Create your models here.

from SNAJ_Cirugias.apps.utilidades.Choices import TiposProcedimiento 

class Modalidad(models.Model):

    class Meta:
        db_table = 'Modalidad'

    idModalidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=60)

class Procedimiento(models.Model):

    class Meta:
        db_table = 'Procedimiento'

    codigoProcedimiento = models.CharField(max_length=10,primary_key=True)
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(max_length=30, choices=TiposProcedimiento.TIPOS_PROC)

class ProcedimientoModalidad(models.Model):

    class Meta:
        db_table = 'ProcedimientoModalidad'

    idProcedimientoModalidad = models.AutoField(primary_key=True)
    codigoProcedimiento = models.ForeignKey(Procedimiento,related_name='modalidadesProc', on_delete=models.CASCADE)
    idModalidad = models.ForeignKey(Modalidad,related_name='modalidades',on_delete=models.CASCADE)
    camaUCI = models.BooleanField()
    bancoSangre = models.BooleanField()
