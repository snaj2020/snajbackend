from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from SNAJ_Cirugias.apps.gestionEquipos.models import *
from SNAJ_Cirugias.apps.gestionEquipos.serializers import * 
from SNAJ_Cirugias.apps.utilidades import Choices

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
# Create your views here.

@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def addAgendaEquipo(request):
    try:
        request_data = JSONParser().parse(request)
        result = saveAgendaEquipo(request_data)
        serializer = result[1]
        
        if(result[0]==True):
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def saveAgendaEquipo(request_data):
    serializer = None
    if(type(request_data)==list):
        serializer = AgendaEquipoSerializer(data=request_data,many=True)
    else:
        serializer = AgendaEquipoSerializer(data=request_data)
    if(serializer.is_valid()):
        serializer.save()
        return (True,serializer) 
    else:
        return (False,serializer) 

@api_view(["PUT"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def editAgendaEquipo(request):
    try:
        request_data = JSONParser().parse(request)
        agendaEquipo = AgendaEquipo.objects.get(pk=request_data.get("id"))
        serializer = AgendaEquipoSerializer(agendaEquipo,data=request_data)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def validarEquipoRequerido(idAgendaEquipo):
    """
    valida si un Equipo/Instrumento esta en
    Equipos requeridos del procedimiento
    Return: True si es requerido o false de lo contrario
    """
    #obtengo los equipos requeridos con el idAgendaProcedimiento
    agendaEquipo = AgendaEquipo.objects.get(id=idAgendaEquipo)
    codigoEquipo = agendaEquipo.codigoEquipo.codigoEquipo
    agendaProcedimiento = AgendaProcedimiento.objects.get(idAgendaProcedimiento=agendaEquipo.idAgendaProcedimiento.idAgendaProcedimiento)
    procedimientoModalidad = ProcedimientoModalidad.objects.get(idProcedimientoModalidad=agendaProcedimiento.idProcedimientoModalidad.idProcedimientoModalidad)
    equiposRequeridos = EquipoRequerido.objects.filter(idProcedimientoModalidad=procedimientoModalidad.idProcedimientoModalidad)
    for equipo in equiposRequeridos:
        if(codigoEquipo == equipo.codigoEquipo.codigoEquipo):
            return True
    return False

@api_view(["DELETE"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def deleteAgendaEquipo(request,idEqu):
    try:
        #Si el equipo no es requerido se puede eliminar
        if(validarEquipoRequerido(idEqu)==False):
            AgendaEquipo.objects.get(id=idEqu).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'error':'El equipo es requerido y no se puede eliminar'},safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#List Agenda Equipos
@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def listAgendaEquipo(request,idAgenProc):
    result = []
    try:
        agendaEquipos = AgendaEquipo.objects.filter(idAgendaProcedimiento_id=idAgenProc).order_by('codigoEquipo')
        for agendaEquipo in agendaEquipos:
            agenEquipo = dict()
            try:
                equipo= Equipo.objects.get(pk=agendaEquipo.codigoEquipo.codigoEquipo)
                agenEquipo.update(
                    nombre=equipo.nombre,
                    descripcion=equipo.descripcion
                )
            except Equipo.DoesNotExist:
                agenEquipo.update(
                    nombre="null",
                    descripcion="null"
                )
            agenEquipo.update(
                id=agendaEquipo.pk,
                codigoEquipo=agendaEquipo.codigoEquipo.codigoEquipo,
                cantidad=agendaEquipo.cantidad,
                estado=agendaEquipo.estado,
                requerido=validarEquipoRequerido(agendaEquipo.pk)
            )
            agendaEquipo_copy = agenEquipo.copy()
            result.append(agendaEquipo_copy)
        #return JsonResponse({'equipos':serializer.data},safe=False,status=status.HTTP_200_OK)
        return JsonResponse(result,safe=False,status=status.HTTP_200_OK)
 
    except AgendaEquipo.DoesNotExist:
        return JsonResponse({'error':'No existe agenda proc con id'},safe=False,status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def getEstadosAgendaEqu(request):
    try:
        estadosAgendaEqu = Choices.Estados.ESTADOS_AGENDA_EQU
        return JsonResponse({'estadosAgendaEqu': estadosAgendaEqu}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getAllEquipos(request):
    try:
        equipos = Equipo.objects.all().order_by('codigoEquipo')
        equipo_serializer = EquipoSerializer(equipos,many=True)
        return JsonResponse(equipo_serializer.data,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
