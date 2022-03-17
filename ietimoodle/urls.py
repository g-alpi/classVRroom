from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/<int:userid>', views.dashboard, name='dashboard'),
    path('<int:exerciseid>/<int:alumnid>', views.delivery, name='delivery'),
]