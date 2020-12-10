from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from SNAJ_Cirugias.apps.gestionSalas.models import Sala
from SNAJ_Cirugias.apps.gestionSalas.serializers import SalaSerializer
from SNAJ_Cirugias.apps.utilidades import Choices

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

# Create your views here.
@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getAllSalas(request):
    try:
        salas = Sala.objects.all().order_by('idSala')
        sala_serializer = SalaSerializer(salas,many=True)
        return JsonResponse(sala_serializer.data,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getEstadosSalas(request):
    try:
        estadosSalas = Choices.Estados.ESTADOS_SALA
        return JsonResponse({'estadosSalas': estadosSalas}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getSalaConId(request, idSal):
    try:
        salaObj = Sala.objects.get(idSala=idSal)
        sala_serializer = SalaSerializer(salaObj)
        return JsonResponse(sala_serializer.data, safe=False, status=status.HTTP_200_OK)
    except Sala.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_400_BAD_REQUEST)