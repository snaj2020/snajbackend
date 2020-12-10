from django.db import models
# Create your models here.
from SNAJ_Cirugias.apps.gestionProcedimientos.models import ProcedimientoModalidad
from SNAJ_Cirugias.apps.agendamiento.models import AgendaProcedimiento
from SNAJ_Cirugias.apps.utilidades.Choices import Estados
#region import models

class Material(models.Model):

    class Meta:
        db_table = 'Material'

    codigoMaterial = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=60)
    unidad = models.CharField(max_length=20)

class MaterialRequerido(models.Model):

    class Meta:
        db_table = 'MaterialRequerido'

    codigoMaterial = models.ForeignKey(Material,on_delete=models.CASCADE)
    idProcedimientoModalidad = models.ForeignKey(ProcedimientoModalidad,on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class AgendaMaterial(models.Model):

    class Meta:
        db_table = 'AgendaMaterial'
        unique_together = [['codigoMaterial', 'idAgendaProcedimiento']]

    codigoMaterial = models.ForeignKey(Material,on_delete=models.CASCADE)
    idAgendaProcedimiento = models.ForeignKey(AgendaProcedimiento,on_delete=models.CASCADE)
    estado = models.CharField(max_length=15,choices=Estados.ESTADOS_AGENDA_MAT,default=Estados.POR_SOLICITAR)
    casaMedica = models.CharField(max_length=60, null=True, blank=True)
    fechaSolicitud = models.DateField(null=True,blank=True)
    fechaEstimada = models.DateField(null=True,blank=True)
    fechaRecibido = models.DateField(null=True,blank=True)
    cantidad = models.IntegerField(default=0)