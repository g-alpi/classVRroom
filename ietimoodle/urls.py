from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/<int:userid>', views.dashboard, name='dashboard'),
    path('dashboard/curso/<int:cursoid>', views.curso, name='curso'),
    path('<int:exerciseid>/<int:alumnid>', views.delivery, name='delivery'),
]

urlpatterns += staticfiles_urlpatterns()