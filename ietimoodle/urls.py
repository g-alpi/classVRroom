from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

app_name='moodle'

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('archivos/<str:element>/<str:filename>', views.download, name='download'),
    path('grade/<int:cursoid>', views.grade, name='grade'),
    path('resource/<int:resourceid>', views.resource, name='resource'),
    path('exercise/<int:exerciseid>', views.exercise, name='exercise'),
    path('<int:exerciseid>/<int:alumnid>', views.delivery, name='delivery'),
]

urlpatterns += staticfiles_urlpatterns()
