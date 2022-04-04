from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import *
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
import random 

def verifyToken(token):
    verifica = False
    for userTk in Token.objects.all():
        if(token==userTk.key):
            verifica = True
            
    return verifica
    
@api_view(['GET'])
def login(request):
    try: 
        correo=(request.GET['email'])
        password=(request.GET['password'])
    except:
        correo=""
        password=""
        _token="null"
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
    try:
        token = (request.GET['token'])
    except:
        token = "null"
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
    try:
        token = (request.GET['token'])
        
    except:
        token = "null"
    verifica = verifyToken(token)
    if (verifica):
        cursos = (Curso.objects.all())
        _curso = request.GET['courseID']
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
            _message = "OK"
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
 
@api_view(['GET'])
def pin_request(request):
    token = (request.GET['token'])
    task = (request.GET['task'])
    verifica = verifyToken(token)
    pinexiste = True
    if (verifica):
        for entrega in Entrega.objects.all():
            if (task == str(entrega.id)):
                if (entrega.pin==None):
                    while (pinexiste==True):
                        print("girando")
                        pinexiste = False
                        newpin = random.randint(0,9999)
                        for entr in Entrega.objects.all():
                            if(newpin == entr.pin):
                                pinexiste = True
                        if (pinexiste == False):
                            break
                    pin = newpin
                    entrega.pin = newpin
                    entrega.save()
                else:
                    pin = entrega.pin
        entrega = Entrega.objects.filter(id=task).first()
        _status = "OK"
        _message = "token va bien"
    else:
        _status = "ERRROR" 
        _message = "invalid token"   

    return JsonResponse({"status":_status,"message":_message,"PIN":entrega.pin})

@api_view(['GET'])
def start_vr_exercise(request):
    pin = (request.GET['pin'])
    exer = False
    for entrega in Entrega.objects.all():
        if (pin==str(entrega.pin)):
            exer = True
            _username = (entrega.user.username)
            _VRexerciseID = (entrega.ejercicio.id)
            _minExerciseVersion = (entrega.ejercicio.minVersion)
            if(status.HTTP_200_OK):
                _status = "OK"
                _message = "OK"
            else:
                exer = False
                _status = "ERROR"
                _message = "failed request"
    if exer ==   False:
        _status="OK"
        _message = "invalid PIN"  
        _username = "null"
        _VRexerciseID = "null"
        _minExerciseVersion = "null"
    return JsonResponse({"status":_status,
                        "message":_message,
                        "username":_username,
                        "VRexerciseID":_VRexerciseID,
                        "minExerciseVersion":_minExerciseVersion})

#Send values as request HEADER
@api_view(['POST'])
def finish_vr_exercise(request):
    _status="ERROR"
    try :
            pin = (request.headers['pin'])
    except: 
            pin = "null"
    try:             
        autograde = (request.headers['autograde'])
    except:
        autograde = "null"
    try: 
        vrexerciseid = (request.headers['exerciseID'])
    except:
        vrexerciseid = "null"
    try:
        exerciseversion = (request.headers['version'])
    except:
        exerciseversion = "null"
    try:
        performancedata = (request.headers['performance'])
    except: 
        performancedata = "null"
    if(pin=="null"):
        _message = "Missing pin"
    elif(autograde == "null"):
        _message = "Missing autograde"
    elif(vrexerciseid == "null"):
        _message = "Missing vrexerciseid"
    elif(exerciseversion == "null"):
        _message = "Missing exerciseversion"
    elif(performancedata == "null"):
        _message = "Missing performancedata"
    else:
        _status = "OK"
        _message = "Exercise data succesfully stored"

    if not (status.HTTP_200_OK):
        _status = "ERROR"
        _message = "failed request"
    
    return JsonResponse({"status": _status, "message":_message})


# {"_id": 
#     {"$oid": "622794b2acc0dbccea8388b4"},  
#     "subscribers":{
#         "teachers": [      1,      2    ],
#         "students": [      3,      4    ]  
#     },
#     "elements": [    
#         {"ID": 1,
#         "type": "HTML",
#         "title": "Traslado de pacientes",
#         "description": "Información sobre el traslado de pacientes",
#         "order": 1,
#         "contents": "<h1>Apuntes de traslado de pacientes</h1><p>El traslado ...</p>"},
#         {"ID": 2,
#         "type": "file",
#         "title": "Primeros auxilios",
#         "description": "Información sobre primeros auxilios",
#         "order": 2,
#         "file": "file:///media/apuntes.pdf"}  
#     ],
#     "tasks": [
#         {"ID": 3,
#         "type": "file",
#         "title": "Cambio a postura lateral",
#         "description": "Inmovilización de pacientes en cama",
#         "order": 1,
#         "uploads": [
#             {"studentID": 3,
#             "text": "Entrega del ejercicio 1",
#             "file": "Ejercicio1-lola.pdf",
#             "grade": 8,
#             "feedback": "Buen trabajo"},
#             {"studentID": 4,
#             "text": "Entrega del ejercicio 1",
#             "file": "Ejercicio1-pepe.pdf",
#             "grade": 6,
#             "feedback": "Buen trabajo"} 
#         ]},
#         {"ID": 4,
#         "type": "HTML",
#         "title": "Cambio a postura frontal",
#         "description": "Inmovilización de pacientes en cama de manera frontal",
#         "order": 2,
#         "uploads": [
#             {"studentID": 3,
#             "text": "loren ipsum dolo sit amet...",
#             "grade": 5,
#             "feedback": "Hay que mejorar"},
#             {"studentID": 4,
#             "text": "lorem ipsum chiquito de la calzada...",
#             "grade": 3,
#             "feedback": "Hay que mejorar"}
#         ]}], 
#     "vr_tasks": [
#         {"ID": 5,
#         "title": "Movilización hacia el borde de la cama",
#         "descripcion": "lorem ipsum movilización borde de la cama",
#         "VRexID": 22,
#         "versionID": 26,
#         "pollID": 1,
#         "completions": [
#             {"studentID": 3,
#                 "position_data": {"data": "...to be decided..."},
#                 "autograde": {"passed_items": 5,"failed_items": 3,"comments": "...to be decided..."},
#                 "grade": 7,"feedback": "Mala postura lateral, riesgo de esguince"},
#             {"studentID": 4,
#                 "position_data": {"data": "...to be decided..."},
#                 "autograde": {"passed_items": 6,"failed_items": 2,"comments": "...to be decided..."},
#                 "grade": 8,"feedback": "Buena postura lateral, mejora tobillo"}
#         ]},
#         {"ID": 6,
#         "title": "Movilización al cabecero de la cama",
#         "descripcion": "lorem impsum movilización cabecero",
#         "VRexID": 23,
#         "versionID": 26,
#         "pollID": 1,
#         "completions": [    
#             {"studentID": 3,
#                 "position_data": {"data": "...to be decided..."},
#                 "autograde": {"passed_items": 1,"failed_items": 7,"comments": "...to be decided..."},
#                 "grade": 2,"feedback": "Mala posición lumbares. Pasos incompletos."},
#             {"studentID": 2,
#                 "position_data": {"data": "...to be decided..."},
#                 "autograde": {"passed_items": 6,"failed_items": 2,"comments": "...to be decided..."},
#                 "grade": 8,"feedback": "Buena postura frontal, mejora tobillo, riesgo de esguince"},
#             {"studentID": 1,
#                 "position_data": {"data": "something something something"},
#                 "autograde": {"passed_items": 5,"failed_items": 5,"score": 5,"comments": "a"},
#                 "_id": {"$oid": "624af77c8ec8cd8d0800e8d4"}
#             },
#             {"studentID": 1,
#                 "position_data": {"data": "something something something"},
#                 "autograde": {"passed_items": 7,"failed_items": 1,"score": 9,"comments": "b"},
#                 "_id": {"$oid": "624af79b8ec8cd8d0800e8d7"}
#             }
#         ]}
#         ],
#     "description": "Movilizaciones 1o A",
#     "title": "Curso 1"}

            
