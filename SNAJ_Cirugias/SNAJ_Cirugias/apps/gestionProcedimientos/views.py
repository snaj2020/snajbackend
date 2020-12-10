from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework.parsers import JSONParser

from SNAJ_Cirugias.apps.gestionProcedimientos.models import *
from .serializers import *

from SNAJ_Cirugias.apps.gestionDocumentos.models import *
from SNAJ_Cirugias.apps.gestionDocumentos.serializers import *

from SNAJ_Cirugias.apps.gestionMateriales.models import *
from SNAJ_Cirugias.apps.gestionMateriales.serializers import *

from SNAJ_Cirugias.apps.gestionEquipos.models import *
from SNAJ_Cirugias.apps.gestionEquipos.serializers import *

from SNAJ_Cirugias.apps.gestionEspecialistas.models import *
from SNAJ_Cirugias.apps.gestionEspecialistas.serializers import *
from SNAJ_Cirugias.apps.utilidades import Choices

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q



# Create your views here.

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getProcedimientoCodigo(request,codProc):
    try:
        procedimiento = Procedimiento.objects.get(codigoProcedimiento=codProc)
        
        serializer = InfoProcedimientoSerializer(procedimiento)
        return JsonResponse({'procedimiento':serializer.data},safe=False,status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getProcedimientoNombre(request,nombreProc):
    try:
        procedimientos = Procedimiento.objects.filter(nombre__icontains=nombreProc)
        serializer = InfoProcedimientoSerializer(procedimientos,many=True)
        return JsonResponse({'procedimientos':serializer.data},safe=False,status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getDocumentosProc(request,codProc,idMod):
    try:
        #procedimiento = Procedimiento.objects.get(codigoProcedimiento=codProc)
        procedimientoMod = ProcedimientoModalidad.objects.filter(codigoProcedimiento=codProc,idModalidad=idMod)
        documentacionRequerida = DocumentacionRequerida.objects.filter(idProcedimientoModalidad__in=procedimientoMod)
        documentos = Documento.objects.filter(codigoDocumento__in=documentacionRequerida.values('codigoDocumento'))
        result = []
        for documento in documentos:
            dicDocRequerida = dict()
            dicDocRequerida.update(
                    codigoDocumento = documento.codigoDocumento,
                    nombre= documento.nombre,
                    descripcion= documento.descripcion,
                    caduca= documento.caduca,
                    id="null",
                    estado = "null",
                    fechaVecimiento = "null",
                    observacion = "null",
                    path = "null",
                    fechaDocRecibido = "null"
                )
            result.append(dicDocRequerida)
        #serializer = DocumentoSerializer(documentos,many=True)
        return JsonResponse(result,safe=False,status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getMaterialesProc(request,codProc,idMod):
    try:
        procedimientoMod = ProcedimientoModalidad.objects.filter(codigoProcedimiento=codProc,idModalidad=idMod)
        materialesRequeridos = MaterialRequerido.objects.filter(idProcedimientoModalidad__in=procedimientoMod).select_related('codigoMaterial')
        #materiales = Material.objects.filter(codigoMaterial__in=materialesRequeridos.values('codigoMaterial'))
        #print(materialesRequeridos.query)
        result = []
        for matRequerido in materialesRequeridos:
            dicMatRequeridos = dict()
            dicMatRequeridos.update(
                    id="null",
                    nombre=matRequerido.codigoMaterial.nombre,
                    unidad=matRequerido.codigoMaterial.unidad,
                    codigoMaterial=matRequerido.codigoMaterial.codigoMaterial,
                    estado="null",
                    casaMedica="null",
                    fechaSolicitud ="null",
                    fechaEstimada = "null",
                    fechaRecibido = "null",
                    cantidad=matRequerido.cantidad
            )
            result.append(dicMatRequeridos)
        #serializer = MaterialRequeridoSerializer(materialesRequeridos,many=True)
        return JsonResponse(result,safe=False,status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getEquiposProc(request,codProc,idMod):
    try:
        procedimientoMod = ProcedimientoModalidad.objects.filter(codigoProcedimiento=codProc,idModalidad=idMod)
        equiposRequeridos = EquipoRequerido.objects.filter(idProcedimientoModalidad__in=procedimientoMod).select_related('codigoEquipo')
        result = []
        for equiipoRequerido in equiposRequeridos:
            dicEquRequerido = dict()
            dicEquRequerido.update(
                nombre=equiipoRequerido.codigoEquipo.nombre,
                descripcion=equiipoRequerido.codigoEquipo.descripcion,
                id="null",
                codigoEquipo=equiipoRequerido.codigoEquipo.codigoEquipo,
                cantidad=equiipoRequerido.cantidad,
                estado="null",
            )
            result.append(dicEquRequerido)
        
        #serializer = EquipoRequeridoSerializer(equiposRequeridos,many=True)
        return JsonResponse(result,safe=False,status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getEspecialidadesProc(request,codProc,idMod):
    try:
        procedimientoMod = ProcedimientoModalidad.objects.filter(codigoProcedimiento=codProc,idModalidad=idMod)
        especialidadesRequeridas = EspecialidadRequerida.objects.filter(idProcedimientoModalidad__in=procedimientoMod).select_related('codigoEspecialidad')
        result = []
        for espRequerida in especialidadesRequeridas:
            dicEspRequeridas = dict()
            dicEspRequeridas.update(
                id="null",
                codigoEspecialidad=espRequerida.codigoEspecialidad.codigoEspecialidad,
                nombreEspecialidad=espRequerida.codigoEspecialidad.nombre,
                cantidad=espRequerida.cantidad,
                registroMedico= "null",
                identificacion= "null",
                nombreEspecialista= "null",
                estado="null"
            )
            result.append(dicEspRequeridas)
        #serializer = EspecialidadRequeridaSerializer(especialidadesRequeridas,many=True)
        return JsonResponse(result,safe=False,status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getTiposProc(request):
    try:
        tiposProc= Choices.TiposProcedimiento.TIPOS_PROC
        return JsonResponse({'tiposProc': tiposProc}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def listAllProcedimientos(request):
    try:
        procedimientos = Procedimiento.objects.all().order_by('codigoProcedimiento') 
        serializer = ProcedimientoSerializer(procedimientos, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.ADMIN_USER).count() > 0)
@transaction.atomic
def addProcedimiento(request):
    '''
        Se crea el procedimiento y con su id se crea ProcedimientoModalidad.
        Con idProcedimientoModalidad, se crean los registros para DocRequerido, MatRequerido, EquRequerido y EspRequerido
        Si hay un error en el almacenamiento de algun registro se hace un rollback
    '''
    request_data = JSONParser().parse(request)

    #Primero se crea el Procedimiento
    proc = dict()
    proc.update(
        codigoProcedimiento=request_data.get("codigoProcedimiento"),
        nombre=request_data.get("nombre"),
        tipo=request_data.get("tipo")
    )
    proc_serializer = ProcedimientoSerializer(data=proc)
    
    if proc_serializer.is_valid(raise_exception=True):
        proc_creado=proc_serializer.save()
    
    #Crear ProcedimientoModalidad
    procMod = dict()
    procMod.update(
        codigoProcedimiento=proc_creado.pk,
        idModalidad=request_data.get("idModalidad"),
        camaUCI=request_data.get("camaUCI"),
        bancoSangre=request_data.get("bancoSangre")
    )
    procMod_serializer = ProcedimientoModalidadSerializer(data=procMod)

    if procMod_serializer.is_valid(raise_exception=True):
        procMod_creado=procMod_serializer.save()
    
    #Para Documentacion Requerida
    listDocsRequeridos = request_data.get("documentacionRequerida")
    for docRequerido in listDocsRequeridos:
        docRequerido.update(
            idProcedimientoModalidad=procMod_creado.pk
        )
    
    docRequerido_serializer = DocumentacionRequeridaSerializer(data=listDocsRequeridos, many=True)
    
    if docRequerido_serializer.is_valid(raise_exception=True):
        docRequerido_serializer.save()
   
    #Para Material Requerido
    listMatsRequeridos = request_data.get("materialesRequeridos")
    for matRequerido in listMatsRequeridos:
        matRequerido.update(
            idProcedimientoModalidad=procMod_creado.pk
        )
    matRequerido_serializer = MaterialRequeridoSerializer(data=listMatsRequeridos, many=True)
    
    if matRequerido_serializer.is_valid(raise_exception=True):
        matRequerido_serializer.save()
    #Para Equipo Requerido
    listEqusRequeridos = request_data.get("equiposRequeridos")
    for equRequerido in listEqusRequeridos:
        equRequerido.update(
            idProcedimientoModalidad=procMod_creado.pk
        )
    equRequerido_serializer = EquipoRequeridoSerializer(data=listEqusRequeridos, many=True)
    
    if equRequerido_serializer.is_valid(raise_exception=True):
        equRequerido_serializer.save()
    
    #Para Equipo Requerido
    listEspRequeridos = request_data.get("especialidadesRequeridas")
    for espRequerido in listEspRequeridos:
        espRequerido.update(
            idProcedimientoModalidad=procMod_creado.pk
        )
    espRequerido_serializer = EspecialidadRequeridaSerializer(data=listEspRequeridos, many=True)
    
    if espRequerido_serializer.is_valid(raise_exception=True):
        espRequerido_serializer.save()
     
    return HttpResponse(status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getProcedimientoNombreIgual(request,nombreProc):
    try:
        procedimiento = Procedimiento.objects.get(nombre=nombreProc)
        serializer = InfoProcedimientoSerializer(procedimiento)
        return JsonResponse(serializer.data,safe=False,status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def listAllModalidades(request):
    try:
        modalidades = Modalidad.objects.all()
        serializer = ModalidadSerializer(modalidades, many=True)
        return JsonResponse(serializer.data,safe=False,status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.ADMIN_USER).count() > 0)
def deleteProcedimiento(request, codProc):
    try:
        Procedimiento.objects.get(pk=codProc).delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
