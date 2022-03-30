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
from .api import *

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/curso/<int:cursoid>', views.curso, name='curso'),
    path('<int:exerciseid>/<int:alumnid>', views.delivery, name='delivery'),
    path('api/login',login),
    path('api/logout',logout),
    path('api/get_courses',get_courses),
    path('api/get_course_details',get_course_details),
    path('api/pin_request',pin_request),
    path('api/start_vr_exercise',start_vr_exercise), 
    path('api/finish_vr_exercise',finish_vr_exercise) 

]

urlpatterns += staticfiles_urlpatterns()
