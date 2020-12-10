from rest_framework import serializers 
from SNAJ_Cirugias.apps.agendamiento.models import AgendaProcedimiento


class AgendaProcedimientoSerializer(serializers.ModelSerializer):
    fechaHora = serializers.DateTimeField(format="%Y-%m-%d %I:%M %p", input_formats=["%Y-%m-%d %I:%M %p"])
    class Meta:
        model = AgendaProcedimiento
        fields = ['idAgendaProcedimiento', 'idProcedimientoModalidad', 'idSala', 'idAcudiente', 'idPaciente', 'idUsuario', 'fechaHora', 'estadoFecha', 'cama', 'estadoCama', 'bancoSangre', 'estadoSala', 'observacion']


