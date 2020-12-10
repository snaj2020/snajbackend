from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, UserAdminEditSerializer, UserEditSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.hashers import make_password

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q

@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.ADMIN_USER).count() > 0)
def addUser(request):
    try:
        request_data = JSONParser().parse(request)
        pss = request_data.get("password")
        request_data.update(
            password=make_password(pss)
        )
        serializer = UserSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_201_CREATED)
        else:
            return JsonResponse(serializer.errors,safe=False,status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(["PUT"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.ADMIN_USER).count() > 0)
def editUserAdmin(request):
    try:
        usuario = User.objects.get(id=request.data.get("id"))
        serializer = UserAdminEditSerializer(usuario,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_200_OK)            
        else:
            return JsonResponse(serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def editUserUser(request):
    try:
        usuario = User.objects.get(id=request.data.get("id"))
        serializer = UserEditSerializer(usuario,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,safe=False,status=status.HTTP_200_OK)            
        else:
            return JsonResponse(serializer.errors,safe=False, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def changePasswordUser(request):
    request_data = JSONParser().parse(request)
    username = request.user
    password = request_data.get('old_password')
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_active:
            user.set_password(request_data.get("new_password"))  
            user.save()             
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    else:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.ADMIN_USER).count() > 0)
def changePasswordAdmin(request):
    request_data = JSONParser().parse(request)  
    user = User.objects.get(id=request_data.get('id'))
    if user is not None:
        if user.is_active:
            user.set_password(request_data.get("new_password"))  
            user.save()             
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    else:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getUser(request,username):
    try:
        usuario = User.objects.get(username=username)
        serializer = UserSerializer(usuario)
        return JsonResponse(serializer.data,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getUserConId(request,idUser):
    try:
        usuario = User.objects.get(pk=idUser)
        serializer = UserSerializer(usuario)
        return JsonResponse(serializer.data,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["DELETE"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(name=settings.ADMIN_USER).count() > 0)
def deleteUser(request,username):
    try:
        usuario = User.objects.get(username=username)
        usuario.is_active=False
        usuario.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def listActiveUsers(request):
    try:
        usuarios = User.objects.filter(is_active=True)
        serializer = UserSerializer(usuarios, many=True)
        return JsonResponse(serializer.data,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def logout(request):
    try:
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#@api_view(["POST"])
@csrf_exempt
def login(request):
    if request.method == "POST":
        try:
            request_data = JSONParser().parse(request)
            username = request_data.get('username')
            password = request_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    token = Token.objects.get_or_create(user=user)                   
                    return JsonResponse({'token':str(token[0])}, safe=False,status=status.HTTP_200_OK)
                else:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            else:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@csrf_exempt
def getUserGroupWithToken(request):
    try:
        #Se obtiene el valor de la clave Authorization, la cual tiene el token del usuario
        authorization = request.headers.get("Authorization")
        token = authorization.split(' ')[-1]
        tokenObj = Token.objects.get(pk=token)        
        user = User.objects.get(pk=tokenObj.user.id)
        grps = user.groups.all()
        result = dict()
        result.update(
            username=str(tokenObj.user),
            group_id=grps[0].pk,
            group_name=grps[0].name
        )
        return JsonResponse(result,safe=False, status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False, json_dumps_params={'ensure_ascii':False},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.core.mail import EmailMultiAlternatives

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def resetPassword(request,toEmail):
    '''send_mail(
    'Subject',
    'Message.',
    None,
    [toEmail],
    )
    '''
    subject= 'Reestablecer Contraseña'
    text_content = 'Recibimos tu solicitud para reestablecer tu contrase&ntilde;a. A continuaci&oacute;n&nbsp; encontrar&aacute;l el c&oacute;digo para cambiarla:'
    html_content = '<h2>Reestablecer Contrase&ntilde;a</h2><p>Recibimos tu solicitud para reestablecer tu contrase&ntilde;a.<br />A continuaci&oacute;n&nbsp; encontrar&aacute;l el c&oacute;digo para cambiarla:</p>'
    msg = EmailMultiAlternatives(subject, text_content, None, [toEmail])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return Response(status=status.HTTP_200_OK)

@api_view(["GET"])
@csrf_exempt
@user_passes_test(lambda u: u.groups.filter(Q(name=settings.ADMIN_USER) | Q(name=settings.AUXILIAR_USER)).count() > 0)
def getGroups(request):
    try:
        grupos = Group.objects.all()
        print(grupos)
        listResult = []
        for grupo in grupos:            
            dicTemp = dict()
            dicTemp.update(
                group_id=grupo.pk,
                group_name=grupo.name
            )
            listResult.append(dicTemp)
        return JsonResponse(listResult,safe=False, json_dumps_params={'ensure_ascii':False},status=status.HTTP_200_OK)
    except Exception as e:
        return JsonResponse({'error':str(e)},safe=False,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
