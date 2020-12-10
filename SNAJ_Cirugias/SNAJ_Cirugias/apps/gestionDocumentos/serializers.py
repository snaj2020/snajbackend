#region imports 
from rest_framework import serializers 
from SNAJ_Cirugias.apps.gestionDocumentos.models import Documento, DocumentoAdjunto, DocumentacionRequerida
#endRegion

class DocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documento
        fields = ['codigoDocumento', 'nombre', 'descripcion', 'caduca']

class DocumentoAdjuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentoAdjunto
        fields = ['id','idAgendaProcedimiento', 'codigoDocumento', 'estado', 'fechaVecimiento', 'path', 'fechaDocRecibido']

class DocumentacionRequeridaSerializer(serializers.ModelSerializer):
    #codigoDocumento = DocumentoSerializer(many=False, read_only=True)
    class Meta:
        model = DocumentacionRequerida
        fields = ['idProcedimientoModalidad', 'codigoDocumento']



