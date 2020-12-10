from django.db import models
from django.conf import settings
# Create your models here.

#region import models
from SNAJ_Cirugias.apps.gestionProcedimientos.models import ProcedimientoModalidad 
from SNAJ_Cirugias.apps.gestionSalas.models import Sala
from SNAJ_Cirugias.apps.gestionPacientes.models import Persona
from SNAJ_Cirugias.apps.utilidades.Choices import Estados
#endregion

class AgendaProcedimiento(models.Model):

    class Meta:
        db_table = 'AgendaProcedimiento'

    idAgendaProcedimiento = models.AutoField(primary_key = True)
    idProcedimientoModalidad = models.ForeignKey(ProcedimientoModalidad,on_delete=models.CASCADE)
    idSala = models.ForeignKey(Sala, null = True, blank = True,on_delete=models.CASCADE)
    idAcudiente = models.ForeignKey(Persona, related_name='Acudiente', null = False, blank = False,on_delete=models.CASCADE)
    idPaciente = models.ForeignKey(Persona, related_name='Paciente', null = False, blank = False,on_delete=models.CASCADE)
    idUsuario = models.ForeignKey(settings.AUTH_USER_MODEL, null = False, blank = False,on_delete=models.CASCADE)
    fechaHora = models.DateTimeField(null=True,blank=True)
    estadoFecha = models.CharField(max_length=15,choices=Estados.ESTADOS_AGENDA_PROC, default=Estados.PENDIENTE)
    cama = models.BooleanField()
    estadoCama = models.CharField(max_length=15,choices=Estados.ESTADOS_CAMA, null=True, blank=True, default=Estados.PENDIENTE)
    bancoSangre = models.BooleanField()
    estadoSala = models.CharField(max_length=30,choices=Estados.ESTADOS_SALA,default=Estados.PENDIENTE)
    observacion = models.CharField(max_length=500,null=True,blank=True)
