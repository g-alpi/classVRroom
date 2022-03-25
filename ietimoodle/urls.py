from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken import views as apiviews
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from rest_framework import routers
from rest_framework import routers, serializers, viewsets
from .models import *
from .serializers import *
from django.core import serializers
import json 
from rest_framework import status
from rest_framework.authtoken.models import Token

@api_view(['GET'])
def login(request):
    correo=(request.GET['email'])
    password=(request.GET['password'])
    for user in User.objects.all():
        if (correo == user.correo):
            print(user.id)
            print(user)
            token = Token.objects.delete(user=user)
            print(token.key)
        return JsonResponse({"user":user.id})

def get_courses(request):
    cursos = (Curso.objects.all())
    allcursos = []
    for curso in cursos:
        profesores = []
        alumnos = []
        suscripciones = Suscripcion.objects.filter(curso=curso.id)
        print("personas en el cursito")
        print(suscripciones)
        for sus in suscripciones:
            if (sus.tipo == 'profesor'):
                user = User.objects.get(username=sus.user)
                print(user.first_name)
                print(user.last_name)
                profesores.append({"first_name":user.first_name,"last_name":user.last_name})
                print(profesores)
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
    return JsonResponse({"status":_status,"message":"message","course_list":allcursos}, safe=False,status=status.HTTP_200_OK)
 
urlpatterns = [
    path('api/login',login),

    path('api/get_courses',get_courses)
]

# urlpatterns = [
#     path(r'^',include(router.urls)),
#     # path('', views.home, name='home'),
#     # path('logout', views.logout_view, name='logout'),
#     # path('dashboard/', views.dashboard, name='dashboard'),
#     # path('dashboard/curso/<int:cursoid>', views.curso, name='curso'),
#     # path('<int:exerciseid>/<int:alumnid>', views.delivery, name='delivery'),
#     path(r'api/',include('rest_framework.urls'))

# ]

urlpatterns += staticfiles_urlpatterns()
