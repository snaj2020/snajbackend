#region imports 
from rest_framework import serializers 
from django.db import models
from SNAJ_Cirugias.apps.gestionMateriales.models import Material, MaterialRequerido, AgendaMaterial
#endRegion

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['codigoMaterial', 'nombre', 'unidad']

class MaterialRequeridoSerializer(serializers.ModelSerializer):
    #codigoMaterial = MaterialSerializer(many=False)
    class Meta:
        model = MaterialRequerido
        fields = ['codigoMaterial', 'idProcedimientoModalidad', 'cantidad']

class AgendaMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgendaMaterial
        fields = ['id','codigoMaterial', 'idAgendaProcedimiento', 'estado','casaMedica','fechaSolicitud','fechaEstimada','fechaRecibido','cantidad']





