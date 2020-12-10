#region imports 
from rest_framework import serializers 
from SNAJ_Cirugias.apps.gestionEspecialistas.models import Especialista, Especialidad, EspecialidadRequerida, AgendaEspecialista
#endRegion


class EspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialista
        fields = ['idEspecialista', 'idPersona', 'registroMedico']

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['codigoEspecialidad', 'nombre']

class EspecialidadRequeridaSerializer(serializers.ModelSerializer):
    #codigoEspecialidad = EspecialidadSerializer(many=False)
    class Meta:
        model = EspecialidadRequerida
        fields = ['codigoEspecialidad', 'idProcedimientoModalidad', 'cantidad']

class AgendaEspecialistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaEspecialista
        fields = ['id','codigoEspecialidad','idAgendaProcedimiento', 'idEspecialista', 'estado']





