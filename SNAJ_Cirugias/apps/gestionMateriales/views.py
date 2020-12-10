from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from SNAJ_Cirugias.apps.gestionMateriales.models import *
from SNAJ_Cirugias.apps.gestionMateriales.serializers import * 
from SNAJ_Cirugias.apps.utilidades import Choices

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
# Create your views here.

@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def addAgendaMaterial(request):
    try:
        request_data = JSONParser().parse(request)
        result = saveAgendaMaterial(request_data)
        serializer = result[1]
        if(result[0]==True):
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def saveAgendaMaterial(request_data):
    
    serializer = None
    if(type(request_data)==list):
        serializer = AgendaMaterialSerializer(data=request_data,many=True)
    else:
        serializer = AgendaMaterialSerializer(data=request_data)
    if(serializer.is_valid()):
        serializer.save()
        return (True,serializer) 
    else:
        return (False,serializer) 

@api_view(["PUT"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def editAgendaMaterial(request):
    try:
        request_data = JSONParser().parse(request)
        agendaMaterial = AgendaMaterial.objects.get(pk=request_data.get("id"))
        serializer = AgendaMaterialSerializer(agendaMaterial,data=request_data)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def validarMaterialRequerido(idAgendaMaterial):
    """
    valida si un material esta en
    los materiales requeridos del procedimiento
    Return: True si es requerido o false de lo contrario
    """
    #obtengo los materiales requeridos con el idAgendaProcedimiento
    agendaMaterial = AgendaMaterial.objects.get(id=idAgendaMaterial)
    codigoMaterial = agendaMaterial.codigoMaterial.codigoMaterial
    agendaProcedimiento = AgendaProcedimiento.objects.get(idAgendaProcedimiento=agendaMaterial.idAgendaProcedimiento.idAgendaProcedimiento)
    procedimientoModalidad = ProcedimientoModalidad.objects.get(idProcedimientoModalidad=agendaProcedimiento.idProcedimientoModalidad.idProcedimientoModalidad)
    materialesRequeridos = MaterialRequerido.objects.filter(idProcedimientoModalidad=procedimientoModalidad.idProcedimientoModalidad)
    for material in materialesRequeridos:
        if(codigoMaterial == material.codigoMaterial.codigoMaterial):
            return True
    return False

@api_view(["DELETE"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def deleteAgendaMaterial(request,idAgenMat):
    try:
        #Si el material no es requerido se puede eliminar
        if(validarMaterialRequerido(idAgenMat)==False):
            AgendaMaterial.objects.get(id=idAgenMat).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'error':'El material es requerido y no se puede eliminar'},safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def getEstadosAgendaMat(request):
    try:
        estadosAgendaMat= Choices.Estados.ESTADOS_AGENDA_MAT
        return JsonResponse({'estadosAgendaMat': estadosAgendaMat}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#List Agenda Materiales
@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def listAgendaMaterial(request,idAgenProc):
    result = []
    try:
        agendaMateriales = AgendaMaterial.objects.filter(idAgendaProcedimiento_id=idAgenProc).order_by('codigoMaterial')
        for agendaMaterial in agendaMateriales:
            agenMaterial = dict()
            try:
                material= Material.objects.get(pk=agendaMaterial.codigoMaterial.codigoMaterial)
                agenMaterial.update(
                    id=agendaMaterial.pk,
                    nombre=material.nombre,
                    unidad=material.unidad
                )
            except Material.DoesNotExist:
                agenMaterial.update(
                    nombre="null",
                    unidad="null"
                )
            agenMaterial.update(
                codigoMaterial=agendaMaterial.codigoMaterial.codigoMaterial,
                estado=agendaMaterial.estado,
                casaMedica=agendaMaterial.casaMedica,
                fechaSolicitud =agendaMaterial.fechaSolicitud,
                fechaEstimada = agendaMaterial.fechaEstimada,
                fechaRecibido = agendaMaterial.fechaRecibido,
                cantidad=agendaMaterial.cantidad,
                requerido=validarMaterialRequerido(agendaMaterial.pk)
            )
            agenMaterial_copy = agenMaterial.copy()
            result.append(agenMaterial_copy)
        #return JsonResponse({'equipos':serializer.data},safe=False,status=status.HTTP_200_OK)
        return JsonResponse(result,safe=False,status=status.HTTP_200_OK)
 
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getAllMateriales(request):
    try:
        materiales = Material.objects.all().order_by('codigoMaterial')
        material_serializer = MaterialSerializer(materiales,many=True)
        return JsonResponse(material_serializer.data,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
