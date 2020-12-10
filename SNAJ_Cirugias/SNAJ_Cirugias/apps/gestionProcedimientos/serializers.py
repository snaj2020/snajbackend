#region imports 
from rest_framework import serializers 
from SNAJ_Cirugias.apps.gestionProcedimientos.models import *
from SNAJ_Cirugias.apps.gestionDocumentos.serializers import *
#endRegion

class ModalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalidad
        fields = ['idModalidad', 'nombre']

class ProcedimientoModalidadSerializer(serializers.ModelSerializer):
    #idModalidad=ModalidadSerializer(many=False,read_only=True)
    #documentos = DocumentacionRequeridaSerializer(many=True,read_only=True)
    class Meta:
        model = ProcedimientoModalidad
        fields = ['idProcedimientoModalidad', 'codigoProcedimiento', 'idModalidad','camaUCI','bancoSangre']


class ProcedimientoSerializer(serializers.ModelSerializer):
    #modalidades=ProcedimientoModalidadSerializer(many=True,read_only=True)
    
    class Meta:
        model = Procedimiento
        fields = ['codigoProcedimiento','nombre','tipo']


class InfoProcedimientoSerializer(serializers.ModelSerializer):
    modalidadesProc = ProcedimientoModalidadSerializer(many=True,read_only=True)
    class Meta:
        model = Procedimiento
        fields = ['codigoProcedimiento','nombre','tipo','modalidadesProc']

