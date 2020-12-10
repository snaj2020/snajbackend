from django.db import models
from django.core.validators import FileExtensionValidator
# Create your models here.

#region import models

from SNAJ_Cirugias.apps.gestionProcedimientos.models import ProcedimientoModalidad
from SNAJ_Cirugias.apps.agendamiento.models import AgendaProcedimiento
from SNAJ_Cirugias.apps.utilidades.Choices import Estados
#endRegion

class Documento(models.Model):

    class Meta:
        db_table = 'Documento'

    codigoDocumento = models.CharField(max_length=10,primary_key=True)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=200,null=True,blank=True)
    caduca = models.BooleanField(default=False)

class DocumentoAdjunto(models.Model):
    class Meta:
        db_table = 'DocumentoAdjunto'

    idAgendaProcedimiento = models.ForeignKey(AgendaProcedimiento,on_delete=models.CASCADE)
    codigoDocumento = models.ForeignKey(Documento,on_delete=models.CASCADE)
    estado = models.CharField(max_length=15, choices=Estados.ESTADOS_DOCUMENTO_ADJ, default=Estados.PENDIENTE)
    fechaVecimiento = models.DateField(null=True,blank=True)
    observacion = models.CharField(max_length=500,null=True,blank=True)
    path = models.FileField(upload_to='Documents/%Y/%m/%d', max_length=500,validators=[FileExtensionValidator(allowed_extensions=['pdf'])],null=True,blank=True)
    fechaDocRecibido = models.DateField(null=True,blank=True)

class DocumentacionRequerida(models.Model):
    class Meta:
        db_table = 'DocumentacionRequerida'
    idProcedimientoModalidad = models.ForeignKey(ProcedimientoModalidad,related_name='documentos',on_delete=models.CASCADE)
    codigoDocumento = models.ForeignKey(Documento,on_delete=models.CASCADE)



    
