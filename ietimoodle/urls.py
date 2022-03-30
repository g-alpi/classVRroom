from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken import views as apiviews
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import routers
from rest_framework import routers, serializers, viewsets
from .models import *
from .serializers import *
from django.core import serializers
import json 
from . import api

app_name='moodle'   

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('archivos/<str:element>/<str:filename>', views.download, name='download'),
    path('grade/<int:cursoid>', views.grade, name='grade'),
    path('qualifications/<int:cursoid>', views.qualifications, name='qualifications'),
    path('resource/<int:resourceid>', views.resource, name='resource'),
    path('exercise/<int:exerciseid>', views.exercise, name='exercise'),
    path('fc/<int:exerciseid>', views.fastcorrection, name='fastcorrection'),
    path('<int:exerciseid>/<int:alumnid>', views.delivery, name='delivery'),
    path('api/login',api.login),
    path('api/logout',api.logout),
    path('api/get_courses',api.get_courses),
    path('api/get_course_details',api.get_course_details),
    path('api/pin_request',api.pin_request),
    path('api/start_vr_exercise',api.start_vr_exercise), 
    path('api/finish_vr_exercise',api.finish_vr_exercise),
    path('actualizar/<int:entrega>/<int:nota>/<str:comentarioProfesor>/<int:estadoEntrega>',views.actualizarEjercicioIndiviual, name="actualizarEjercicio"),
    path('actualizar/<int:entrega>/<int:nota>/<str:comentarioProfesor>',views.actualizar, name="actualizar"),
]

urlpatterns += staticfiles_urlpatterns()
