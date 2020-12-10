from django.shortcuts import render
from rest_framework import status

from SNAJ_Cirugias.apps.gestionPacientes.models import Persona
from SNAJ_Cirugias.apps.gestionPacientes.serializers import PersonaSerializer
from SNAJ_Cirugias.apps.utilidades import Choices

from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

# Create your views here.
@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getPersonaIdentificacion(request, idenPersona):
    try:
        personas = Persona.objects.filter(identificacion__istartswith=idenPersona)
        personas_serializer = PersonaSerializer(personas, many=True)
        return JsonResponse({'personas': personas_serializer.data}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getTiposIdentificacion(request):
    try:
        tiposId = Choices.TiposID.TIPOS_ID
        return JsonResponse({'tiposID': tiposId}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.ADMIN_USER).count() > 0)
def addPersona(request):
    if request.method == 'POST':
        persona_data = JSONParser().parse(request)
        print(persona_data)
        # retrieve the person using identification
        resultSavePersona = savePersona(persona_data)
        if resultSavePersona[0] == 0:
            return JsonResponse(resultSavePersona[1].data, safe=False, status=status.HTTP_200_OK)
        elif resultSavePersona[0]==1:
            return JsonResponse(resultSavePersona[1].data, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(resultSavePersona[1].errors, status=status.HTTP_400_BAD_REQUEST)


def savePersona(persona_data):
    try:
        identificacionPersona = persona_data.get("identificacion")
        person = Persona.objects.get(identificacion=identificacionPersona)
        persona_serializer = PersonaSerializer(person, data=persona_data)
        if persona_serializer.is_valid():
            persona_serializer.save()
            return (0, persona_serializer)
        else:
            return(2, persona_serializer)
    except Persona.DoesNotExist:  # if person does not exist then add persona
        persona_serializer = PersonaSerializer(data=persona_data)
        if persona_serializer.is_valid():
            persona_serializer.save()
            return (1,persona_serializer)
        return (2,persona_serializer)
