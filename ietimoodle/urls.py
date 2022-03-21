from django.urls import path

from . import views


urlpatterns = [
    path('<int:exerciseid>/<int:alumnid>', views.index, name='index'),
    
    
]