# region imports
from django.shortcuts import render
from rest_framework import status
from SNAJ_Cirugias.apps.agendamiento.models import AgendaProcedimiento
from SNAJ_Cirugias.apps.agendamiento.serializers import AgendaProcedimientoSerializer
from SNAJ_Cirugias.apps.gestionEquipos.models import EquipoRequerido, AgendaEquipo
#from SNAJ_Cirugias.apps.gestionEquipos.serializers import EquipoRequeridoSerializer
from SNAJ_Cirugias.apps.gestionMateriales.models import MaterialRequerido, AgendaMaterial
#from SNAJ_Cirugias.apps.gestionMateriales.serializers import MaterialRequerido
from SNAJ_Cirugias.apps.gestionEspecialistas.models import EspecialidadRequerida, AgendaEspecialista
#from SNAJ_Cirugias.apps.gestionEspecialistas.serializers import EspecialidadRequeridaSerializer
from SNAJ_Cirugias.apps.gestionPacientes.models import Persona
from SNAJ_Cirugias.apps.gestionSalas.models import Sala
from SNAJ_Cirugias.apps.gestionDocumentos.models import Documento, DocumentacionRequerida, DocumentoAdjunto
from SNAJ_Cirugias.apps.gestionProcedimientos.models import ProcedimientoModalidad, Procedimiento
from SNAJ_Cirugias.apps.gestionProcedimientos.serializers import ProcedimientoModalidadSerializer
from SNAJ_Cirugias.apps.gestionPacientes.serializers import PersonaSerializer
from SNAJ_Cirugias.apps.gestionEquipos.views import saveAgendaEquipo
from SNAJ_Cirugias.apps.gestionMateriales.views import saveAgendaMaterial
from SNAJ_Cirugias.apps.gestionEspecialistas.views import saveAgendaEspecialista
from SNAJ_Cirugias.apps.gestionDocumentos.views import saveDocumentoAdjunto, getListDocAdjunto
from SNAJ_Cirugias.apps.utilidades import Choices

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound, FileResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime,timedelta



#3rd library
#import PyPDF2 
import locale
#locale.setlocale(locale.LC_TIME, 'es-US') 
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
# endRegion


# Create your views here.
#Variable para considerar persona Menor de Edad
menorEdad = 18


# region Methods
def extraerInformacionPaciente(request_data):

    resultDict = dict()
    resultDict.update(
        identificacion=request_data.get("identificacionPac"),
        tipoIdentificacion=request_data.get("tipoIdentificacionPac"),
        fechaNacimiento=request_data.get("fechaNacimientoPac"),
        correo=request_data.get("correoPac"),
        telefono=request_data.get("telefonoPac"),
        direccion=request_data.get("direccionPac"),
        nombre=request_data.get("nombrePac"),
        genero=request_data.get("generoPac")
    )
    return resultDict


def extraerInformacionAcudiente(request_data):
    resultDict = dict()
    resultDict.update(
        identificacion=request_data.get("identificacionAcu"),
        tipoIdentificacion=request_data.get("tipoIdentificacionAcu"),
        fechaNacimiento=request_data.get("fechaNacimientoAcu"),
        correo=request_data.get("correoAcu"),
        telefono=request_data.get("telefonoAcu"),
        direccion=request_data.get("direccionAcu"),
        nombre=request_data.get("nombreAcu"),
        genero=request_data.get("generoAcu")
    )
    return resultDict


def verificarCamposObligatoriosPersona(persona_data):
    if (persona_data.get("identificacion") is None or
        persona_data.get("tipoIdentificacion") is None or
        persona_data.get("fechaNacimiento") is None or
        persona_data.get("genero") is None or
        persona_data.get("telefono") is None or
        persona_data.get("direccion") is None or
            persona_data.get("nombre") is None):
        return True
    else:
        return False

def addAgendaEquipos(idAgendaProc, idProcModalidad):
    result = []

    equiposRequeridos = EquipoRequerido.objects.filter(
        idProcedimientoModalidad=idProcModalidad)

    for equipoRequerido in equiposRequeridos:
        agendaEquipo = dict()
        agendaEquipo.update(
            codigoEquipo=equipoRequerido.codigoEquipo.codigoEquipo,
            idAgendaProcedimiento=idAgendaProc,
            estado="PEND",
            cantidad=equipoRequerido.cantidad
        )
        agendaEquipo_copy = agendaEquipo.copy()
        result.append(agendaEquipo_copy)

    return saveAgendaEquipo(result)

def addAgendaMateriales(idAgendaProc, idProcModalidad):
    result = []

    materialesRequeridos = MaterialRequerido.objects.filter(
        idProcedimientoModalidad=idProcModalidad)
    for materialRequerido in materialesRequeridos:
        agendaMaterial = dict()
        agendaMaterial.update(
            codigoMaterial=materialRequerido.codigoMaterial.codigoMaterial,
            idAgendaProcedimiento=idAgendaProc,
            estado="PSOL",
            cantidad=materialRequerido.cantidad
        )
        agendaMaterial_copy = agendaMaterial.copy()
        result.append(agendaMaterial_copy)
    return saveAgendaMaterial(result)

def addDocumentosRequeridos(idAgendaProc, idProcModalidad):
    result = []

    documentosRequeridos = DocumentacionRequerida.objects.filter(
        idProcedimientoModalidad=idProcModalidad)
    for documentacionRequerida in documentosRequeridos:
        docAdjunto = dict()
        docAdjunto.update(
            codigoDocumento=documentacionRequerida.codigoDocumento.codigoDocumento,
            idAgendaProcedimiento=idAgendaProc,
            estado="PEND"
        )
        docAdjunto_copy = docAdjunto.copy()
        result.append(docAdjunto_copy)
    return saveDocumentoAdjunto(result)

def getCodDocumentoConsentimientoPadres():
    nombreDocConsentimientoPadres="CONSENTIMIENTO DE PADRES"
    try:
        documentoConsentimientoPadres = Documento.objects.filter(nombre__icontains=nombreDocConsentimientoPadres)
        return documentoConsentimientoPadres[0].codigoDocumento
    except Documento.DoesNotExist:
        return -1
    

def addDocumentoConsentimientoPadres(idAgendaProc):
    result = []
    docAdjunto = dict()
    docAdjunto.update(
        codigoDocumento=getCodDocumentoConsentimientoPadres(),
        idAgendaProcedimiento=idAgendaProc,
        estado="PEND"
    )
    docAdjunto_copy = docAdjunto.copy()
    result.append(docAdjunto_copy)
    return saveDocumentoAdjunto(result)

def addAgendaEspecialista(idAgendaProc, idProcModalidad):
    result = []

    especialidadesRequeridas = EspecialidadRequerida.objects.filter(
        idProcedimientoModalidad=idProcModalidad)
    for especialidadRequerida in especialidadesRequeridas:
        for iterator in range(0, especialidadRequerida.cantidad):
            agendaEspecialista = dict()
            agendaEspecialista.update(
                codigoEspecialidad=especialidadRequerida.codigoEspecialidad.codigoEspecialidad,
                idAgendaProcedimiento=idAgendaProc,
                estado="PEND")
            agendaEspecialista_copy = agendaEspecialista.copy()
            result.append(agendaEspecialista_copy)
    return saveAgendaEspecialista(result)

def calcularEdadPaciente(fechaNacimiento):

    fNacimiento = datetime.strptime(fechaNacimiento, "%Y-%m-%d").date()
    hoy=date.today()
    edad=hoy.year - fNacimiento.year - ((hoy.month,hoy.day)< (fNacimiento.month,fNacimiento.day))
    return edad   

def isPacienteMenorEdad(agendaPro_pk, fechaNacimientoPaciente):
    edad=calcularEdadPaciente(fechaNacimientoPaciente)
    if(edad<menorEdad):
        return True
    else:
        return False

def getDatosAgendaProc(agendaProcedimiento):
    agenProc = dict()
    agenProc.update(
        idAgendaProcedimiento=agendaProcedimiento.idAgendaProcedimiento,
        idProcedimientoModalidad=agendaProcedimiento.idProcedimientoModalidad.idProcedimientoModalidad,
        idSala=agendaProcedimiento.idSala.idSala,
        fechaHora=agendaProcedimiento.fechaHora.strftime("%Y-%m-%d %I:%M %p"),
        estadoFecha=agendaProcedimiento.estadoFecha,
        cama=agendaProcedimiento.cama,
        estadoCama=agendaProcedimiento.estadoCama,
        bancoSangre=agendaProcedimiento.bancoSangre,
        estadoSala=agendaProcedimiento.estadoSala,
        observacion=agendaProcedimiento.observacion,
        idUsuario=agendaProcedimiento.idUsuario.id,
        nombreUsuarioCreador=agendaProcedimiento.idUsuario.username
        )
            
    try:
        sala = Sala.objects.get(pk=agendaProcedimiento.idSala.idSala)
        agenProc.update(nombreSala=sala.nombre)
    except Exception as e:
         agenProc.update(nombreSala="null")
    
    try:
        paciente = Persona.objects.get(pk=agendaProcedimiento.idPaciente.idPersona)
        agenProc.update(
            idPaciente=paciente.idPersona,
            tipoIdentificacionPac=paciente.tipoIdentificacion,
            identificacionPac=paciente.identificacion,
            nombrePac = paciente.nombre,
            fechaNacPac = paciente.fechaNacimiento
        )
                
    except Exception as e:
        agenProc.update(
            idPaciente="null",
            tipoIdentificacionPac="null",
            identificacionPac="null",
            nombrePac = "null",
            fechaNacPac = "null"
        )

    try:
        acudiente = Persona.objects.get(pk=agendaProcedimiento.idAcudiente.idPersona)
        agenProc.update(
            idAcudiente=acudiente.idPersona,
            identificacionAcu=acudiente.identificacion,
            nombreAcu = acudiente.nombre,
            fechaNacAcu = acudiente.fechaNacimiento
            )
    except Exception as e:
        agenProc.update(
            idAcudiente="null",
            identificacionAcu="null",
            nombreAcu = "null",
            fechaNacAcu = "null"
        )
        
    try:
        procModalidad = ProcedimientoModalidad.objects.get(pk=agendaProcedimiento.idProcedimientoModalidad.idProcedimientoModalidad)
        try:
            procedimiento = Procedimiento.objects.get(pk=procModalidad.codigoProcedimiento.codigoProcedimiento)
            agenProc.update(
                codigoProcedimiento=procedimiento.codigoProcedimiento,
                nombreProcedimiento=procedimiento.nombre,
                tipoProcedimiento=procedimiento.tipo
            )
        except Exception as e:
            agenProc.update(
                codigoProcedimiento="null",
                nombreProcedimiento="null",
                tipoProcedimiento="null"
            )    
    except Exception as e:
        agenProc.update(
            codigoProcedimiento="null",
            nombreProcedimiento="null",
            tipoProcedimiento="null"
        )   
    return agenProc

def getDatosAgendasProc(listAgendasProc):
    result=[]
    for agendaProcedimiento in listAgendasProc:
        result.append(getDatosAgendaProc(agendaProcedimiento))
    return result

# endregion


@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def addAgendaProcedimiento(request):
    if request.method == 'POST':
        request_data = JSONParser().parse(request)
        #respuesta=[]
        agendaProc_data = dict()

    # region Para el paciente
        # Se extrae del request la información para paciente
        paciente_data = extraerInformacionPaciente(request_data)

        # Se validan los datos obligatorios para el paciente
        if (verificarCamposObligatoriosPersona(paciente_data)):
            return JsonResponse('error: some Paciente field required is empty', status=status.HTTP_400_BAD_REQUEST)

        # Se verifica si el paciente ya está registrado en la BD
        idPaciente = paciente_data.get("identificacion")
        try:
            # retrieve the person using identification
            paciente = Persona.objects.get(identificacion=idPaciente)
            paciente_serializer = PersonaSerializer(
                paciente, data=paciente_data)
            if paciente_serializer.is_valid():
                pacienteActualizado=paciente_serializer.save()
                # Se asigna el pk de paciente a la Agenda Procedimiento
                agendaProc_data.update(idPaciente=pacienteActualizado.pk)
                
                #Se agrega la información actualizada a la respuesta
                #respuesta.append({'paciente':paciente_serializer.data})
            # return JsonResponse({'persona':persona_serializer.data},safe=False,status=status.HTTP_200_OK)
        except Persona.DoesNotExist:  # if person does not exist then add persona
            paciente_serializer = PersonaSerializer(data=paciente_data)
            if paciente_serializer.is_valid():
                pacienteCreado = paciente_serializer.save()
                agendaProc_data.update(idPaciente=pacienteCreado.pk)

                #Se agrega la información actualizada a la respuesta
                #respuesta.append({'paciente':paciente_serializer.data})
                # return JsonResponse(paciente_serializer.data, status=status.HTTP_201_CREATED)
            # return JsonResponse(paciente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
    # endRegion

    # region Para el acudiente
        # Se extrae del request la información para paciente
        acudiente_data = extraerInformacionAcudiente(request_data)

        # Se validan los datos obligatorios para el acudiente
        if (verificarCamposObligatoriosPersona(acudiente_data)):
            return JsonResponse('error: some Acudiente field required is empty', status=status.HTTP_400_BAD_REQUEST)

        # Se verifica si el acudiente ya está registrado en la BD
        idAcudiente = acudiente_data.get("identificacion")
        try:
            # retrieve the person using identification
            acudiente = Persona.objects.get(identificacion=idAcudiente)
            acudiente_serializer = PersonaSerializer(
                acudiente, data=acudiente_data)
            if acudiente_serializer.is_valid():
                acudienteActualizado = acudiente_serializer.save()
                # Se asigna el pk de paciente a la Agenda Procedimiento
                agendaProc_data.update(idAcudiente=acudienteActualizado.pk)

                #Se agrega la información actualizada de acudiente a la respuesta
                #respuesta.append({'acudiente':acudiente_serializer.data})
            # return JsonResponse({'persona':persona_serializer.data},safe=False,status=status.HTTP_200_OK)
        except Persona.DoesNotExist:  # if person does not exist then add persona
            acudiente_serializer = PersonaSerializer(data=acudiente_data)
            if acudiente_serializer.is_valid():
                acudienteCreado = acudiente_serializer.save()
                # Se asigna el pk de paciente a la Agenda Procedimiento
                agendaProc_data.update(idAcudiente=acudienteCreado.pk)

                #Se agrega la información actualizada de acudiente a la respuesta
                #respuesta.append({'acudiente':acudiente_serializer.data})
                # return JsonResponse(paciente_serializer.data, status=status.HTTP_201_CREATED)
            # return JsonResponse(paciente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        
    # endRegion
    # region Datos de Agenda de Procedimiento
        # Para la observación
        agendaProc_data.update(observacion=request_data.get("observacion"))

        # Para el ProcedimientoModalidad
        agendaProc_data.update(
            idProcedimientoModalidad=request_data.get("idProcedimientoModalidad"))

        # Para la Sala
        agendaProc_data.update(idSala=request_data.get("idSala"))
        agendaProc_data.update(estadoSala=request_data.get("estadoSala"))

        # Para idUsuario
        agendaProc_data.update(idUsuario=request_data.get("idUsuario"))

        # Para la fechaHora
        agendaProc_data.update(fechaHora=request_data.get("fechaHora"))

        # Para el estadoFecha
        agendaProc_data.update(estadoFecha=request_data.get("estadoFecha"))

        # Para la cama
        agendaProc_data.update(cama=request_data.get("cama"))

        # Para el estadoCama
        agendaProc_data.update(estadoCama=request_data.get("estadoCama"))

        # Para el bancoSangre
        agendaProc_data.update(bancoSangre=request_data.get("bancoSangre"))
    # endRegion

    # region Crear AgendaProcedimiento
        # Se crea el serializaer con los datos obtenidos
        agendaProc_serializer = AgendaProcedimientoSerializer(
            data=agendaProc_data)
        # Si el serializer es válido se crea el registro
        if agendaProc_serializer.is_valid():
            agendaProcCreada = agendaProc_serializer.save()

            #Se agrega la información actualizada de acudiente a la respuesta
            
            #respuesta.append({'agendaProcedimiento':agendaProc_serializer.data})

            #Se agrega a la agendaEquipos los equipos requeridos para la AgendaProc creada
            resultAddAgendaEquipos = addAgendaEquipos(agendaProcCreada.pk,agendaProcCreada.idProcedimientoModalidad)
            if(resultAddAgendaEquipos[0]==False):
                return JsonResponse(resultAddAgendaEquipos[1].errors, safe=False, status=status.HTTP_400_BAD_REQUEST)    
            #else:
                #respuesta.append({'agendaEquipos':resultAddAgendaEquipos[1].data})
            #Se agrega a la AgendaMaterial los materiales requeridos para la AgendaProc creada
            resultAddAgendaMateriales = addAgendaMateriales(agendaProcCreada.pk,agendaProcCreada.idProcedimientoModalidad)
            if(resultAddAgendaMateriales[0]==False):
                return JsonResponse(resultAddAgendaMateriales[1].errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
            #else:
                #respuesta.append({'agendaMateriales':resultAddAgendaMateriales[1].data})

            #Se agrega a la AgendaEspecialista las especialiades requeridas para la AgendaProc creada
            resultAddAgendaEspecialista = addAgendaEspecialista(agendaProcCreada.pk,agendaProcCreada.idProcedimientoModalidad)
            if(resultAddAgendaEspecialista[0]==False):
                return JsonResponse(resultAddAgendaEspecialista[1].errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
            #else:
                #respuesta.append({'agendaEspecialistas':resultAddAgendaEspecialista[1].data})
            
            #Se agrega a la Documento Adjunto los documentos requeridos para la AgendaProc creada
            resultAddDocumentosRequeridos =addDocumentosRequeridos(agendaProcCreada.pk,agendaProcCreada.idProcedimientoModalidad)
            if(resultAddDocumentosRequeridos[0]==False):
                return JsonResponse(resultAddDocumentosRequeridos[1].errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
            else:
                documentosAdjuntos= list()

                documentosAdjuntos=resultAddDocumentosRequeridos[1].data.copy()
                #Se verifica si el paciente es menor de edad
                if(isPacienteMenorEdad(agendaProcCreada.pk,paciente_data.get('fechaNacimiento'))):
                    #Si es menor de edad se agrega a la documentación el consentimiento de padres
                    resultAddDocumentoConsentimientoPadres =addDocumentoConsentimientoPadres(agendaProcCreada.pk)
                    if(resultAddDocumentoConsentimientoPadres[0]==False):
                        return JsonResponse(resultAddDocumentoConsentimientoPadres[1].errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        documentosAdjuntos.append(resultAddDocumentoConsentimientoPadres[1].data[0])
                
                
                #respuesta.append({'documentosAdjuntos':resultAddDocumentosRequeridos[1].data})
                #respuesta.append({'documentosAdjuntos':documentosAdjuntos})
            
            return JsonResponse({'idAgendaProcedimiento':agendaProcCreada.pk}, safe=False, status=status.HTTP_201_CREATED)
            #return JsonResponse(respuesta, safe=False, status=status.HTTP_201_CREATED)
        return JsonResponse(agendaProc_serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    # endRegion


@api_view(["PUT"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def editAgendaProcedimiento(request):
    if request.method == 'PUT':
        request_data = JSONParser().parse(request)
        agendaProc_data = dict()
        agendaProc = None
        agendaProc_OriginalSerializer = dict()
        # Busca la agendaProcedimiento con id
        try:
            agendaProc = AgendaProcedimiento.objects.get(
                idAgendaProcedimiento=request_data.get("idAgendaProcedimiento"))
            agendaProc_OriginalSerializer = AgendaProcedimientoSerializer(agendaProc)
        # Si no existe la agendaProcedimiento
        except AgendaProcedimiento.DoesNotExist:
            return JsonResponse({'error': 'The AgendaProcedimiento does not exist'}, status=status.HTTP_404_NOT_FOUND)

    # region Para el paciente
        # Se validan los datos para el paciente       
        if(request_data.get("correoPac") is None or
            request_data.get("telefonoPac") is None or
            request_data.get("direccionPac") is None ):
            return JsonResponse('error: some Paciente field required is empty', status=status.HTTP_400_BAD_REQUEST)

        # Se obtiene el paciente de la AgendaProcedimiento
        idPac = agendaProc_OriginalSerializer.data.get("idPaciente")
        try:
            # retrieve the person using id
            paciente = Persona.objects.get(idPersona=idPac)
            paciente_OriginalSerializer = PersonaSerializer(paciente)
            paciente_data=dict()
            paciente_data.update(
                identificacion= paciente_OriginalSerializer.data.get("identificacion"),
                tipoIdentificacion=paciente_OriginalSerializer.data.get("tipoIdentificacion"),
                fechaNacimiento=paciente_OriginalSerializer.data.get("fechaNacimiento"),
                correo=request_data.get("correoPac"),
                telefono=request_data.get("telefonoPac"),
                direccion=request_data.get("direccionPac"),
                nombre=paciente_OriginalSerializer.data.get("nombre"),
                genero=paciente_OriginalSerializer.data.get("genero"),
                )

            paciente_serializer = PersonaSerializer(
                paciente, data=paciente_data)
            if paciente_serializer.is_valid():
                pacienteActualizado=paciente_serializer.save()
                # Se asigna el pk de paciente a la Agenda Procedimiento
                agendaProc_data.update(idPaciente=pacienteActualizado.pk)
            # return JsonResponse({'persona':persona_serializer.data},safe=False,status=status.HTTP_200_OK)
            else:
                return JsonResponse('error: Paciente not found', status=status.HTTP_400_BAD_REQUEST)
        except Persona.DoesNotExist:  # if person does not exist then add persona
            return JsonResponse('error: Paciente not found', status=status.HTTP_400_BAD_REQUEST)
            #paciente_serializer = PersonaSerializer(data=paciente_data)
            #if paciente_serializer.is_valid():
            #    pacienteCreado = paciente_serializer.save()
            #    Se asigna el pk de paciente a la Agenda Procedimiento
            #    agendaProc_data.update(idPaciente=pacienteCreado.pk)


    # endRegion

    # region Para el acudiente
        # Se extrae del request la información para paciente
        acudiente_data = extraerInformacionAcudiente(request_data)

        # Se validan los datos obligatorios para el acudiente
        if (verificarCamposObligatoriosPersona(acudiente_data)):
            return JsonResponse('error: some Acudiente field required is empty', status=status.HTTP_400_BAD_REQUEST)

        # Se verifica si el acudiente ya está registrado en la BD
        identificacionAcudiente = acudiente_data.get("identificacion")
        try:
            # retrieve the person using identification
            acudiente = Persona.objects.get(identificacion=identificacionAcudiente)
            #acudiente_data['identificacion'] = acudiente.get("identificacion")
            acudiente_serializer = PersonaSerializer(
                acudiente, data=acudiente_data)
            if acudiente_serializer.is_valid():
                acudienteActualizado = acudiente_serializer.save()
                # Se asigna el pk de paciente a la Agenda Procedimiento
                agendaProc_data.update(idAcudiente=acudienteActualizado.pk)
            # return JsonResponse({'persona':persona_serializer.data},safe=False,status=status.HTTP_200_OK)
        except Persona.DoesNotExist:  # if person does not exist then add persona
            acudiente_serializer = PersonaSerializer(data=acudiente_data)
            if acudiente_serializer.is_valid():
                acudienteCreado = acudiente_serializer.save()
                # Se asigna el pk de paciente a la Agenda Procedimiento
                agendaProc_data.update(idAcudiente=acudienteCreado.pk)
                # return JsonResponse(paciente_serializer.data, status=status.HTTP_201_CREATED)
            # return JsonResponse(paciente_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # endRegion

    # region Datos de Agenda de Procedimiento
        # Para la observación
        agendaProc_data.update(observacion=request_data.get("observacion"))

        # Para el ProcedimientoModalidad
        agendaProc_data.update(
            idProcedimientoModalidad=agendaProc_OriginalSerializer.data.get('idProcedimientoModalidad'))

        # Para la Sala
        agendaProc_data.update(idSala=request_data.get("idSala"))
        agendaProc_data.update(estadoSala=request_data.get("estadoSala"))

        # Para idUsuario
        agendaProc_data.update(idUsuario=request_data.get("idUsuario"))

        # Para la fechaHora
        agendaProc_data.update(fechaHora=request_data.get("fechaHora"))

        # Para el estadoFecha
        #TODO Si llega agendado -> validar si todo esta listo? cambiar a Agendado: cambiar a estadoAnterior
        if request_data.get("estadoFecha") == Choices.Estados.CONFIRMADO[0]:
            if agenEstadosIsValid(request_data.get("idAgendaProcedimiento")):
                agendaProc_data.update(estadoFecha=request_data.get("estadoFecha"))
            else:
                agendaProc_data.update(estadoFecha=agendaProc_OriginalSerializer.data.get("estadoFecha"))
        else:
            agendaProc_data.update(estadoFecha=request_data.get("estadoFecha"))
        # Para la cama
        agendaProc_data.update(cama=request_data.get("cama"))

        # Para el estadoCama
        #Se verifica si el ProcMod requiere de cama
        procMod = ProcedimientoModalidad.objects.get(pk=agendaProc_OriginalSerializer.data.get("idProcedimientoModalidad"))
        
        if(request_data.get("cama").lower() == "true"):
            agendaProc_data.update(estadoCama=request_data.get("estadoCama"))
        else:
            if(procMod.camaUCI):
                return JsonResponse({'error':"Cama is required by ProcedimientoModalidad"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                agendaProc_data.update(estadoCama=None)    

        # Para el bancoSangre
        agendaProc_data.update(bancoSangre=request_data.get("bancoSangre"))
    # endRegion

    # region Editar Agenda Procedimiento

        # Se mantiene el idPaciente del registro original ya que no es un campo editable
        agendaProc_data['idPaciente'] = agendaProc_OriginalSerializer.data.get("idPaciente")
        # Se crea serializer referenciando el objeto original a modificar con el data especificado
        agendaProc_serializer = AgendaProcedimientoSerializer(
            agendaProc, data=agendaProc_data)
        if agendaProc_serializer.is_valid():
            agendaProc_serializer.save()
            return JsonResponse(agendaProc_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(agendaProc_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # endRegion

@ api_view(["GET"])
@ csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def listAgendaProcedimiento(request):
    result = []
    if request.method == 'GET':
        try:
            agendasProc = AgendaProcedimiento.objects.all().order_by('fechaHora')            
            result = getDatosAgendasProc(agendasProc)

            return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
            # 'safe=False' for objects serialization
        except AgendaProcedimiento.DoesNotExist:
            return JsonResponse({'error': 'AgendaProcedimiento does NOT EXIST'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getEstadosCama(request):
    try:
        estadosCama = Choices.Estados.ESTADOS_CAMA
        return JsonResponse({'estadosCama': estadosCama}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getEstadosAgendaProc(request):
    try:
        estadosAgendaProc = Choices.Estados.ESTADOS_AGENDA_PROC
        return JsonResponse({'estadosAgendaProc': estadosAgendaProc}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def generateRecibido(request, idAgendaProc):
    
    recibidoFileName = "Documents/Reports/recibidoFile.pdf"
    
    docsAdjuntos = getListDocAdjunto(idAgendaProc)
    if(docsAdjuntos[0]):
        

        doc = SimpleDocTemplate(recibidoFileName, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        Story = []
        logotipo = "Documents/Images/logo.png"

        formatoFecha = datetime.now()
        fechaActual = formatoFecha.strftime("%A, %B %d de %Y")
        
        estilos = getSampleStyleSheet()
        estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        texto = '%s' % fechaActual
        Story.append(Paragraph(texto, estilos["Justify"]))
        Story.append(Spacer(1, 20))
        imagen = Image(logotipo, 1 * inch, 1 * inch)
        Story.append(imagen)
        Story.append(Spacer(1, 30))
        Story.append(Paragraph("ACUSE DE RECIBIDO", estilos["Title"]))
        Story.append(Spacer(1, 20))

        #Se obtienen las variables necesarias
        agenProc = AgendaProcedimiento.objects.get(pk=idAgendaProc)
        nombreAuxiliar=request.user.first_name + " " + request.user.last_name
        nombrePaciente = Persona.objects.get(pk=agenProc.idPaciente.idPersona).nombre
        fechaHoraProc = agenProc.fechaHora.strftime("%d de %B del %Y")

        #Consulta para el nombre del procedimiento
        idProcMod = agenProc.idProcedimientoModalidad.idProcedimientoModalidad
        codProc = ProcedimientoModalidad.objects.get(pk=idProcMod).codigoProcedimiento.codigoProcedimiento

        nombreProc = Procedimiento.objects.get(codigoProcedimiento=codProc).nombre

        Story.append(Spacer(1, 12))
        texto = 'Se confirma que el día %s el señor(a) %s a las %s, recibe la siguiente documentación:' % (formatoFecha.strftime("%d de %B del %Y"),
                                                                nombreAuxiliar,
                                                                formatoFecha.strftime("%I:%M %p")
                                                                )
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 25))

        algunDocumento = False
        iterator=1
        for docAdjunto in docsAdjuntos[1]:
            docAdjPath = docAdjunto.get('path')
            docAdjCodigo = docAdjunto.get('codigoDocumento')
            docAdjFechaRec = docAdjunto.get('fechaDocRecibido')
            docAdjNombre = Documento.objects.get(codigoDocumento=docAdjCodigo).nombre
            #Validar que tenga archivo adjunto
            if docAdjPath != "" and docAdjPath!=None:
                algunDocumento=True
                texto = ' %i.  %s con código %s recibido el %s' % (iterator,docAdjNombre, docAdjCodigo, docAdjFechaRec)
                Story.append(Paragraph(texto, estilos["Normal"]))
                iterator += 1
        if not algunDocumento:
            texto = '-NO se ha recibido ningún documento'
            Story.append(Paragraph(texto, estilos["Normal"]))    
        Story.append(Spacer(1, 25))
        texto = 'Del paciente %s, con fecha de programación tentativa de cirugía para el %s para realizar el procedimiento %s.' % (nombrePaciente,fechaHoraProc,nombreProc)
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 20))
        texto = 'Sinceramente,'
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 48))
        texto = '%s' % nombreAuxiliar
        Story.append(Paragraph(texto, estilos["Normal"]))
        Story.append(Spacer(1, 12))
        doc.title="Recibido para "+ nombrePaciente
        doc.build(Story)
        return FileResponse(open(recibidoFileName,'rb'))
    else:
        return JsonResponse({'error':'No existe agenda proc con id'},safe=False,status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def getAgendaProcsConFecha(request, sinceDate, toDate):
    try:
        #Dado que Django no retorna los valores limiteSuperior se debe sumar un día a la fecha toDate
        date = datetime.strptime(toDate, "%Y-%m-%d")
        modified_date = date + timedelta(days=1)
        agendasProc = AgendaProcedimiento.objects.filter(fechaHora__range=[sinceDate, modified_date]).order_by('fechaHora')
        result = getDatosAgendasProc(agendasProc)
        return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def getAgendaProcConId(request, idAgendaProc):
    try:
        agendaProc = AgendaProcedimiento.objects.get(idAgendaProcedimiento=idAgendaProc)
        result = getDatosAgendaProc(agendaProc)

        return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
    except AgendaProcedimiento.DoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def getAgendaProcsConIdenPac(request, idenPac):
    result = []
    try:
        idPac = Persona.objects.get(identificacion=idenPac).idPersona
        agendasProc = AgendaProcedimiento.objects.filter(idPaciente=idPac).order_by('fechaHora')       
        result = getDatosAgendasProc(agendasProc)
        return JsonResponse(result, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
def agenEstadosIsValid(idAgendaProcedimiento):
    """
    Valida el estado de todas las agendas y los documentos adjuntos
    Returns True si todas las agendas estan agendadas y los documentos estan aporbados
    """
    agenProc = AgendaProcedimiento.objects.get(idAgendaProcedimiento = idAgendaProcedimiento)
    
    
    print(agenProc.cama)
    if(agenProc.cama == True):
        if(agenProc.estadoCama != Choices.Estados.AGENDADO[0]):
            return False
    
    if(agenProc.estadoSala != Choices.Estados.AGENDADO[0]):
        return False
    
    #Se validan los estados de los documentos adjuntos
    docAdjuntos = DocumentoAdjunto.objects.filter(idAgendaProcedimiento=idAgendaProcedimiento)
    for docAdj in docAdjuntos:
        if(docAdj.estado != Choices.Estados.APROBADO[0]):
            return False

    #Se validan los estados de la agenda de los equipos            
    agenEquipos = AgendaEquipo.objects.filter(idAgendaProcedimiento=idAgendaProcedimiento)
    for agenEquipo in agenEquipos:
        if(agenEquipo.estado != Choices.Estados.AGENDADO[0]):
            return False

    #Se validan los estados de la agenda de los especialistas            
    agenEspecialistas = AgendaEspecialista.objects.filter(idAgendaProcedimiento=idAgendaProcedimiento)
    for agenEspecialista in agenEspecialistas:
        if(agenEspecialista.estado != Choices.Estados.AGENDADO[0]):
            return False

    #Se validan los estados de la agenda de los materiales            
    agenMateriales = AgendaMaterial.objects.filter(idAgendaProcedimiento=idAgendaProcedimiento)
    for agenMaterial in agenMateriales:
        if(agenMaterial.estado != Choices.Estados.RECIBIDO[0]):
            return False

    return True
    

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.AUXILIAR_USER).count() > 0)
def validarEstadoAgenda(request, idAgendaProcedimiento):
    try:
        if(agenEstadosIsValid(idAgendaProcedimiento)==True):
            return JsonResponse({"estado":str(True)}, safe=False, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"estado":str(False)}, safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
