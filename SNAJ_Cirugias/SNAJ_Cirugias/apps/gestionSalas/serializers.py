#region imports 
from rest_framework import serializers 
from SNAJ_Cirugias.apps.gestionSalas.models import Sala
#endRegion


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['idSala', 'nombre','lugar']




