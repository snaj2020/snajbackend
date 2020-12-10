#region imports 
from rest_framework import serializers 
from SNAJ_Cirugias.apps.gestionPacientes.models import Persona
#endRegion


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ['idPersona', 'identificacion', 'tipoIdentificacion','fechaNacimiento','correo','telefono','direccion','nombre','genero']




