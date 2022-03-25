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

def get_courses(request):
    # campos = Curso.objects.first()._meta.fields
    # print(campos)
    # for campo in campos:
    #     print(campo)
    
    curso = (Curso.objects.first())
    curso = json.dumps(curso.toJson(),indent=4)
    print(curso)
    # for e in cursos:
    #     print(e)
    # "curso = curso.nombre"
    return JsonResponse({
        "course_list":curso,
        })
 
urlpatterns = [
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
