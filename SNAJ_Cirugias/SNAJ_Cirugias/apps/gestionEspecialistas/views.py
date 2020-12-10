from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from SNAJ_Cirugias.apps.gestionEspecialistas.models import *
from SNAJ_Cirugias.apps.gestionEspecialistas.serializers import *
from SNAJ_Cirugias.apps.utilidades import Choices
from SNAJ_Cirugias.apps.gestionPacientes.serializers import PersonaSerializer

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
# Create your views here.

@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def addAgendaEspecialista(request):
    try:
        request_data = JSONParser().parse(request)
        result = saveAgendaEspecialista(request_data)
        serializer = result[1]
        if(result[0]==True):
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def saveAgendaEspecialista(request_data):
    
    serializer = None
    if(type(request_data)==list):
        serializer = AgendaEspecialistaSerializer(data=request_data,many=True)
    else:
        serializer = AgendaEspecialistaSerializer(data=request_data)
    if(serializer.is_valid()):
        serializer.save()
        return (True,serializer) 
    else:
        return (False,serializer) 

@api_view(["PUT"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def editAgendaEspecialista(request):
    try:
        agenEspecialist = dict()
        request_data = JSONParser().parse(request)
        agendaEspecialista = AgendaEspecialista.objects.get(pk=request_data.get("id"))
        agenEspecialist.update(
            estado=request_data.get("estado"),
            idAgendaProcedimiento=agendaEspecialista.idAgendaProcedimiento.idAgendaProcedimiento,
            codigoEspecialidad=agendaEspecialista.codigoEspecialidad.codigoEspecialidad
        )
        
        try:
            person_data=dict()
            personaEspecialista = Persona.objects.get(identificacion=request_data.get("identificacion"))
            person_data.update(
                identificacion=personaEspecialista.identificacion,
                tipoIdentificacion=personaEspecialista.tipoIdentificacion,
                fechaNacimiento=personaEspecialista.fechaNacimiento,
                correo=personaEspecialista.correo,
                telefono=personaEspecialista.telefono,
                direccion=personaEspecialista.direccion,
                nombre=request_data.get("nombreEspecialista"),
                genero=personaEspecialista.genero
            )
            persona_serializer = PersonaSerializer (personaEspecialista,data=person_data) 
            if(persona_serializer.is_valid()):
                persona_serializer.save()
            else:
                return JsonResponse(persona_serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
            try:
                esp_data=dict()
                especialista = Especialista.objects.get(idPersona=personaEspecialista.idPersona)
                esp_data.update(
                    idPersona=especialista.idPersona.idPersona,
                    registroMedico=request_data.get("registroMedico")
                )
                especialista_serializer = EspecialistaSerializer(especialista,data=esp_data)
                if(especialista_serializer.is_valid()):
                    especialista_serializer.save()
                    agenEspecialist.update(
                        idEspecialista=especialista.idEspecialista
                        )
                else:
                    return JsonResponse(especialista_serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
            except Especialista.DoesNotExist:
                esp = dict()
                esp.update (
                    idPersona=personaEspecialista.idPersona,
                    registroMedico=request_data.get("registroMedico")
                )
                esp_serializer = EspecialistaSerializer(data=esp)
                if(esp_serializer.is_valid()):
                    esp_creado = esp_serializer.save()
                    agenEspecialist.update(
                        idEspecialista=esp_creado.idEspecialista
                        )
                else:
                    return JsonResponse(esp_serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
                
        except Persona.DoesNotExist:
            return JsonResponse({'error':'NO existe persona con esa identificación'},safe=False,status=status.HTTP_400_BAD_REQUEST)

        serializer = AgendaEspecialistaSerializer(agendaEspecialista, data=agenEspecialist)

        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def validarEspecialistaRequerido(idAgendaEspecialista):
    """
    valida si una especialidad esta en las especialidades 
    requeridas del procedimiento y no supera la cantidad requerida 
    Return: True si es requerida o false de lo contrario
    """
    #obtengo las especialidades requeridas con el idAgendaProcedimiento
    agendaEspecialista = AgendaEspecialista.objects.get(id=idAgendaEspecialista)
    agendaProcedimiento = AgendaProcedimiento.objects.get(idAgendaProcedimiento=agendaEspecialista.idAgendaProcedimiento.idAgendaProcedimiento)
    procedimientoModalidad = ProcedimientoModalidad.objects.get(idProcedimientoModalidad=agendaProcedimiento.idProcedimientoModalidad.idProcedimientoModalidad)
    especialidadesRequeridas = EspecialidadRequerida.objects.filter(idProcedimientoModalidad=procedimientoModalidad.idProcedimientoModalidad)
    
    #obtengo la cantidad de especialidades agendadas con el codigo de especialidad y el idAgendaProcedimiento
    codigoEspecialidad = agendaEspecialista.codigoEspecialidad.codigoEspecialidad
    idAgendaProcedimiento = agendaEspecialista.idAgendaProcedimiento.idAgendaProcedimiento
    espAgendadas = len(list(AgendaEspecialista.objects.filter(idAgendaProcedimiento=idAgendaProcedimiento,codigoEspecialidad=codigoEspecialidad)))

    for especialidad in especialidadesRequeridas:
        if(codigoEspecialidad == especialidad.codigoEspecialidad.codigoEspecialidad):
            if(especialidad.cantidad>=espAgendadas):
                return True
    return False

@api_view(["DELETE"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def deleteAgendaEspecialista(request,idAgenEsp):
    try:
        #Si la especialidad no es requerido se puede eliminar
        if(validarEspecialistaRequerido(idAgenEsp)==False):
            AgendaEspecialista.objects.get(id=idAgenEsp).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'error':'La especialidad es requerida y no se puede eliminar'},safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def getEstadosEspecialistas(request):
    try:
        estadosEspecialistas = Choices.Estados.ESTADOS_ESPECIALISTA
        return JsonResponse({'estadosEspecialistas': estadosEspecialistas}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def getCantidadRequerida(idAgendaEspecialista):
    """
    Retorna la cantidad de una especialidad requerida para un procedimiento
    Return: retorna la cantidad requerida de una especialidad
    """
    #obtengo las especialidad requerida con el idAgendaProcedimiento
    agendaEspecialista = AgendaEspecialista.objects.get(id=idAgendaEspecialista)
    agendaProcedimiento = AgendaProcedimiento.objects.get(idAgendaProcedimiento=agendaEspecialista.idAgendaProcedimiento.idAgendaProcedimiento)
    procedimientoModalidad = ProcedimientoModalidad.objects.get(idProcedimientoModalidad=agendaProcedimiento.idProcedimientoModalidad.idProcedimientoModalidad)
    codigoEspecialidad = agendaEspecialista.codigoEspecialidad.codigoEspecialidad
    
    try:
        especialidadRequerida = EspecialidadRequerida.objects.get(idProcedimientoModalidad=procedimientoModalidad.idProcedimientoModalidad,codigoEspecialidad=codigoEspecialidad).cantidad
        return especialidadRequerida
    except EspecialidadRequerida.DoesNotExist:
        return 0
    

#List Agenda Especialistas con idAgendaProc
@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def listAgendaEspecialistas(request,idAgenProc):
    result = []
    try:
        agendaEspecialistas = AgendaEspecialista.objects.filter(idAgendaProcedimiento_id=idAgenProc).order_by('codigoEspecialidad')
        contEsp = []
        for agendaEspecialista in agendaEspecialistas:
            agenEspecialista = dict()
            
            agenEspecialista.update(
                id=agendaEspecialista.pk,
                codigoEspecialidad=agendaEspecialista.codigoEspecialidad.codigoEspecialidad
            )
            try:
                especialidad = Especialidad.objects.get(pk=agendaEspecialista.codigoEspecialidad.codigoEspecialidad)
                agenEspecialista.update(
                    nombreEspecialidad=especialidad.nombre
                )
            except Especialidad.DoesNotExist:
                agenEspecialista.update(
                    nombreEspecialidad="null"
                )

            if agendaEspecialista.idEspecialista is not None:
                try:
                    especialista= Especialista.objects.get(idEspecialista=agendaEspecialista.idEspecialista.idEspecialista)
                    agenEspecialista.update(
                        registroMedico=especialista.registroMedico
                    )
                    try:
                        personaEsp = Persona.objects.get(pk=especialista.idPersona.idPersona)
                        agenEspecialista.update(
                            identificacion=personaEsp.identificacion,
                            nombreEspecialista=personaEsp.nombre
                        )
                    except Persona.DoesNotExist:
                        agenEspecialista.update(
                            identificacion="null",
                            nombreEspecialista="null"
                        )
                except Especialista.DoesNotExist:
                    agenEspecialista.update(
                        registroMedico="null",
                        identificacion="null",
                        nombreEspecialista="null"
                    )
            else:
               agenEspecialista.update(
                        registroMedico="null",
                        identificacion="null",
                        nombreEspecialista="null"
                    )     
            
            agenEspecialista.update(
                estado=agendaEspecialista.estado,
            )
            codigoEsp = agendaEspecialista.codigoEspecialidad.codigoEspecialidad
            if(getCantidadRequerida(agendaEspecialista.pk)>contEsp.count(codigoEsp)):
                agenEspecialista.update(
                    requerido=True,
                )
            else:
                agenEspecialista.update(
                    requerido=False,
                )
            contEsp.append(codigoEsp)
            agenEspecialista_copy = agenEspecialista.copy()
            result.append(agenEspecialista_copy)
        #return JsonResponse({'equipos':serializer.data},safe=False,status=status.HTTP_200_OK)
        return JsonResponse(result,safe=False,status=status.HTTP_200_OK)
 
    except AgendaEspecialista.DoesNotExist:
        return JsonResponse({'error':'No existe agenda proc con id'},safe=False,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getAllEspecialidades(request):
    try:
        especialidades = Especialidad.objects.all().order_by('codigoEspecialidad')
        especialidad_serializer = EspecialidadSerializer(especialidades,many=True)
        return JsonResponse(especialidad_serializer.data,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
