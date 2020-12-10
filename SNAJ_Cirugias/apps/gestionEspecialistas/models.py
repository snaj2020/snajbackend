from django.db import models

# Create your models here.

#imports models
from SNAJ_Cirugias.apps.gestionProcedimientos.models import ProcedimientoModalidad
from SNAJ_Cirugias.apps.gestionPacientes.models import Persona
from SNAJ_Cirugias.apps.agendamiento.models import AgendaProcedimiento
from SNAJ_Cirugias.apps.utilidades.Choices import Estados
#endregion

class Especialista(models.Model):

    class Meta:
        db_table = 'Especialista'

    idEspecialista = models.AutoField(primary_key=True)
    idPersona = models.OneToOneField(Persona,on_delete=models.CASCADE)
    registroMedico = models.CharField(max_length=20, unique=True)

class Especialidad(models.Model):

    class Meta:
        db_table = 'Especialidad'

    codigoEspecialidad = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=60)

class EspecialidadRequerida(models.Model):

    class Meta:
        db_table = 'EspecialidadRequerida'

    codigoEspecialidad = models.ForeignKey(Especialidad,on_delete=models.CASCADE)
    idProcedimientoModalidad = models.ForeignKey(ProcedimientoModalidad,on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class AgendaEspecialista(models.Model):

    class Meta:
        db_table = 'AgendaEspecialista'
    codigoEspecialidad = models.ForeignKey(Especialidad,on_delete=models.CASCADE,default="null")
    idAgendaProcedimiento = models.ForeignKey(AgendaProcedimiento,on_delete=models.CASCADE)
    idEspecialista = models.ForeignKey(Especialista,on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(max_length=15,choices=Estados.ESTADOS_ESPECIALISTA, default=Estados.PENDIENTE)
    
