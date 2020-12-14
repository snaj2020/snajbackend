from django.shortcuts import render
from django.http import JsonResponse, FileResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from SNAJ_Cirugias.apps.gestionDocumentos.models import *
from SNAJ_Cirugias.apps.gestionDocumentos.serializers import *
from SNAJ_Cirugias.apps.agendamiento.models import *
from SNAJ_Cirugias.apps.agendamiento.serializers import *
from SNAJ_Cirugias.apps.gestionProcedimientos.models import *
from SNAJ_Cirugias.apps.gestionProcedimientos.serializers import *
from SNAJ_Cirugias.apps.utilidades import Choices
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, FileResponse

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

# Create your views here.

@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def addDocumentoAdjunto(request):
    try:
        #request_data = JSONParser().parse(request)
        result = saveDocumentoAdjunto(request.data)
        serializer = result[1]
        if(result[0]==True):
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def saveDocumentoAdjunto(request_data):
    serializer = None
    if(type(request_data)==list):
        serializer = DocumentoAdjuntoSerializer(data=request_data,many=True)
    else:
        serializer = DocumentoAdjuntoSerializer(data=request_data)
    if(serializer.is_valid()):
        serializer.save()
        return (True,serializer) 
    else:
        return (False,serializer) 

@api_view(["PUT"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def editDocumentoAdjunto(request):
    try:
        #request_data = JSONParser().parse(request)
        documentoAdjunto = DocumentoAdjunto.objects.get(id=request.data.get("id"))
        #Actualiza el archivo adjunto
        DocumentoAdjunto.objects.get(id=request.data.get("id")).path.delete(save=False)
        serializer = DocumentoAdjuntoSerializer(documentoAdjunto,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_201_CREATED)            
        else:
            return JsonResponse(serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def validarDocAdjRequerido(idDocAdjunto):
    """
    valida si un documento adjunto esta en
    la documentacion requerida del procedimiento
    Return: True si es requerida, false si hay mas de un documento
    adjunto del mismo tipo o no es requerido
    """
    #obtengo la documentacion requerida con el idAgendaProcedimiento
    documentoAdjunto = DocumentoAdjunto.objects.get(id=idDocAdjunto)
    codigoDoc = documentoAdjunto.codigoDocumento.codigoDocumento
    idAgendaProcedimiento = documentoAdjunto.idAgendaProcedimiento.idAgendaProcedimiento
    agendaProcedimiento = AgendaProcedimiento.objects.get(idAgendaProcedimiento=idAgendaProcedimiento)
    procedimientoModalidad = ProcedimientoModalidad.objects.get(idProcedimientoModalidad=agendaProcedimiento.idProcedimientoModalidad.idProcedimientoModalidad)
    documentosRequeridos = DocumentacionRequerida.objects.filter(idProcedimientoModalidad=procedimientoModalidad.idProcedimientoModalidad)
    
    contDocAdj = len(list(DocumentoAdjunto.objects.filter(idAgendaProcedimiento = idAgendaProcedimiento, codigoDocumento = codigoDoc)))
    for doc in documentosRequeridos:
        if(codigoDoc == doc.codigoDocumento.codigoDocumento):
            #Si hay mas de un documento del mismo tipo que es requerido
            #solo se deja 1 requerido
            if(contDocAdj==1):
                return True
            else:
                return False
    return False

def getCantidadRequeridos(idDocAdjunto):
    documentoAdjunto = DocumentoAdjunto.objects.get(id=idDocAdjunto)
    codigoDoc = documentoAdjunto.codigoDocumento.codigoDocumento
    idAgendaProcedimiento = documentoAdjunto.idAgendaProcedimiento.idAgendaProcedimiento
    agendaProcedimiento = AgendaProcedimiento.objects.get(idAgendaProcedimiento=idAgendaProcedimiento)
    idProcedimientoModalidad = agendaProcedimiento.idProcedimientoModalidad.idProcedimientoModalidad
    procedimientoModalidad = ProcedimientoModalidad.objects.get(idProcedimientoModalidad=idProcedimientoModalidad)
    contDocRequeridos = len(list(DocumentacionRequerida.objects.filter(idProcedimientoModalidad=idProcedimientoModalidad,codigoDocumento=codigoDoc)))
    return contDocRequeridos

@api_view(["DELETE"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def deleteDocumentoAdjunto(request, idDocAdj):
    try:
        #Si el documento no es requerido se puede eliminar
        if(validarDocAdjRequerido(idDocAdj)==False):
            DocumentoAdjunto.objects.get(id=idDocAdj).path.delete(save=False)
            DocumentoAdjunto.objects.get(id=idDocAdj).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'error':'El documento es requerido y no se puede eliminar'},safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def getEstadosDocAjunto(request):
    try:
        estadosDocAdjunto = Choices.Estados.ESTADOS_DOCUMENTO_ADJ
        return JsonResponse({'estadosDocAdjunto': estadosDocAdjunto}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


#List Agenda Equipos
@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def listDocAdjunto(request,idAgenProc):
    result = getListDocAdjunto(idAgenProc)
    
    if(result[0]):
        return JsonResponse(result[1],safe=False,status=status.HTTP_200_OK)
    else:
        return JsonResponse({'error':'No existe agenda proc con id'},safe=False,status=status.HTTP_400_BAD_REQUEST)

def getListDocAdjunto(idAgenProc):
    result = []
    try:
        docsAdjuntos = DocumentoAdjunto.objects.filter(idAgendaProcedimiento_id=idAgenProc).order_by('codigoDocumento')
        contDoc = []
        for docAdjunto in docsAdjuntos:
            doAdjunto = dict()
            try:
                documento= Documento.objects.get(pk=docAdjunto.codigoDocumento.codigoDocumento)
                doAdjunto.update(
                    nombre=documento.nombre,
                    descripcion=documento.descripcion,
                    caduca=documento.caduca
                )
            except Documento.DoesNotExist:
                doAdjunto.update(
                    nombre="null",
                    descripcion="null",
                    caduca="null"
                )
            doAdjunto.update(
                id=docAdjunto.pk,
                codigoDocumento = docAdjunto.codigoDocumento.codigoDocumento,
                estado = docAdjunto.estado,
                fechaVecimiento = docAdjunto.fechaVecimiento,
                observacion = docAdjunto.observacion,
                path = docAdjunto.path.name,
                fechaDocRecibido = docAdjunto.fechaDocRecibido,
                
            )

            #valido si los documentos adjuntos son requeridos
            codigoDoc = docAdjunto.codigoDocumento.codigoDocumento
            if(getCantidadRequeridos(docAdjunto.pk)>contDoc.count(codigoDoc)):
                doAdjunto.update(
                    requerido=True,
                )
            else:
                doAdjunto.update(
                    requerido=False,
                )
            contDoc.append(codigoDoc)
            doAdjunto_copy = doAdjunto.copy()
            result.append(doAdjunto_copy)
        #return JsonResponse({'equipos':serializer.data},safe=False,status=status.HTTP_200_OK)
        return (True,result)
 
    except DocumentoAdjunto.DoesNotExist:
        return (False,result)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def getArchivoAdjunto(request, idDocAdj):
    adjuntoFileName=""
    try:
        docAdj = DocumentoAdjunto.objects.get(pk=idDocAdj)
        adjuntoFileName = docAdj.path.name
    except DocumentoAdjunto.DoesNotExist:
        return JsonResponse({'error':'No existe documento adjunto con id'},safe=False,status=status.HTTP_400_BAD_REQUEST)
    if adjuntoFileName != "":
        return FileResponse(open(adjuntoFileName,'rb'))
    else:
        return JsonResponse({'error':'El documento adjunto no tiene path'},safe=False,status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getAllDocumentos(request):
    try:
        documentos = Documento.objects.all().order_by('codigoDocumento')
        documento_serializer = DocumentoSerializer(documentos,many=True)
        return JsonResponse(documento_serializer.data,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

