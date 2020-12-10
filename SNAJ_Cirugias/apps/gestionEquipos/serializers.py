#region imports 
from rest_framework import serializers 
from SNAJ_Cirugias.apps.gestionEquipos.models import Equipo, EquipoRequerido, AgendaEquipo
#endRegion


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipo
        fields = ['codigoEquipo', 'nombre', 'descripcion']

class EquipoRequeridoSerializer(serializers.ModelSerializer):
    #codigoEquipo = EquipoSerializer(many=False)
    class Meta:
        model = EquipoRequerido
        fields = ['codigoEquipo', 'idProcedimientoModalidad', 'cantidad']

class AgendaEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaEquipo
        fields = ['id','idAgendaProcedimiento', 'codigoEquipo', 'estado','cantidad']



