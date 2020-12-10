from django.db import models

#region import models
from SNAJ_Cirugias.apps.gestionProcedimientos.models import ProcedimientoModalidad
from SNAJ_Cirugias.apps.agendamiento.models import AgendaProcedimiento
from SNAJ_Cirugias.apps.utilidades.Choices import Estados
#endregion
# Create your models here.

class Equipo(models.Model):
    class Meta:
        db_table = 'Equipo'

    codigoEquipo = models.CharField(max_length=15, primary_key=True)
    nombre = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=200,null=True,blank=True)

class EquipoRequerido(models.Model):
    class Meta:
        db_table = 'EquipoRequerido'
    codigoEquipo = models.ForeignKey(Equipo,on_delete=models.CASCADE)
    idProcedimientoModalidad = models.ForeignKey(ProcedimientoModalidad,on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class AgendaEquipo(models.Model):

    class Meta:
        db_table = 'AgendaEquipo'
        unique_together = [['codigoEquipo', 'idAgendaProcedimiento']]
    
    idAgendaProcedimiento = models.ForeignKey(AgendaProcedimiento,on_delete=models.CASCADE)
    codigoEquipo = models.ForeignKey(Equipo,on_delete=models.CASCADE)
    estado = models.CharField(max_length=15,choices=Estados.ESTADOS_AGENDA_EQU,default=Estados.PENDIENTE)
    cantidad = models.IntegerField(default=0)