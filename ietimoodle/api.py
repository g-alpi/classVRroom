from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import *
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password


def verifyToken(token):
    verifica = False
    for userTk in Token.objects.all():
        if(token==userTk.key):
            verifica = True
            
    return verifica
    
@api_view(['GET'])
def login(request):
    correo=(request.GET['email'])
    password=(request.GET['password'])
    _correo=False
    if (correo==""):
        _message = "email is required"
        _status = "ERROR"
        _token = 'null'
    for user in User.objects.all():
        if (correo == user.correo):
            _correo=True
            if (check_password(password,user.password)):
                try:    
                    token = Token.objects.create(user=user)
                except: 
                    token = Token.objects.get(user=user)
                    _token = token.key
                if(status.HTTP_200_OK):
                    _status = "OK"
                    _message = "OK"
                else:
                    _status = "ERROR"
            else:
                _message = "wrong credentials"
                _status = "ERROR"
                _token = "null" 
    if(_correo==False):
         _message = "Wrong credentials"
         _status = "ERROR" 
         _token = 'null'
    
    return JsonResponse({"status":_status,"message":_message,"token":_token  })

@api_view(['GET'])
def logout(request):
    token = (request.GET['token'])
    verifica = verifyToken(token)
    if (verifica):
        _status = "OK"
        _message = "Session succesfully closed."
    else:        
        _status = "ERROR"
        _message = "session_token is required"

    return JsonResponse({'status': _status, "message":_message})
    


def get_courses(request):
    token = (request.GET['token'])
    verifica = verifyToken(token)
    if (verifica):
        _status = "OK"
        _message = "Session succesfully closed."
        cursos = (Curso.objects.all())
        allcursos = []
        for curso in cursos:
            profesores = []
            alumnos = []
            suscripciones = Suscripcion.objects.filter(curso=curso.id)
            for sus in suscripciones:
                if (sus.tipo == 'profesor'):
                    user = User.objects.get(username=sus.user)
                    profesores.append({"first_name":user.first_name,"last_name":user.last_name})
                else:
                    user = User.objects.get(username=sus.user)
                    alumnos.append({"first_name":user.first_name,"last_name":user.last_name})

            respuesta = {
                "courseID":curso.id,
                "institutionID":curso.centro.id,
                "title":curso.nombre,
                "description":curso.descripcion,
                "subscribers":{
                    "teachers":[
                        profesores
                    ],
                    "alumns":[
                        alumnos
                    ]
                }
            }
            allcursos.append(respuesta)
            if(status.HTTP_200_OK):
                _status = "OK"
            else:
                _status = "ERROR"
    else:        
        _status = "ERROR"
        _message = "session_token is required"
        allcursos = 'null'

    
    return JsonResponse({"status":_status,"message":_message,"course_list":allcursos}, safe=False,status=status.HTTP_200_OK)

@api_view(['GET'])
def get_course_details(request):
    token = (request.GET['token'])
    verifica = verifyToken(token)
    if (verifica):
        cursos = (Curso.objects.all())
        _curso = request.GET['courseID']
        print(_curso)
        _recursos = []
        _ejercicios = []
        resp = False
        for curso in cursos:
            if (_curso == str(curso.id)):
                resp = True
                recursos = Recurso.objects.filter(curso=curso.id)
                ejercicios = Ejercicio.objects.filter(curso=curso.id)
                for recurso in recursos:
                    _recursos.append(recurso.titulo)
                for ejercicio in ejercicios:
                    _ejercicios.append(ejercicio.nombre)
                _course = {
                    "title": curso.nombre,
                    "description":curso.descripcion,
                    "courseID": curso.id,
                    "institutionID": curso.centro.id,
                    "elements": _recursos,
                    "tasks": _ejercicios,
                }
        if(status.HTTP_200_OK):
            _status = "OK"
            _message = "BIEN"
        else:
            _status = "ERROR"
            _message = "failed request"
        if (resp == False):
            _message = "course no found"
            _course = "null"  
    else :
        _status = "ERROR"
        _message = "token required"
        _course = 'null'
          
    return JsonResponse({"status":_status,"message":_message,"course":_course}, safe=False,status=status.HTTP_200_OK)
 