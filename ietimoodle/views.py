import re
from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse
from .forms import LoginForm
from .models import *



class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return render(request, "logout.html")

@login_required
def dashboard(request):
    suscripciones=Suscripcion.objects.filter(user=request.user.pk)
    cursos=Curso.objects.all
    content={
        'suscripciones': suscripciones,
        'cursos':cursos,
    }
    return render(request, 'dashboard.html', content)

@login_required
def curso(request, cursoid):
    return render(request, 'curso.html')

@login_required
def delivery(request, exerciseid, alumnid):
    alumn= get_object_or_404(User, pk=alumnid)
    exercise=get_object_or_404(Ejercicio, pk=exerciseid)
    delivery=Entrega.objects.filter(ejercicio=exercise, user=alumn)[0]
    alumnos= Entrega.objects.filter(ejercicio=exercise)
    alumnosID=[]
    for i in alumnos :
        alumnosID.append(i.user.pk)

    if alumnosID.index(alumnid) == len(alumnosID)-1:
        nextAlumn = alumnosID[0]
    else:
        nextAlumn = alumnosID[alumnosID.index(alumnid) + 1]

    prevAlumn = alumnosID[alumnosID.index(alumnid) - 1]
    
    
    content = {
        'alumn': alumn,
        'exercise': exercise,
        'delivery': delivery,
        'nextAlumn': nextAlumn,
        'prevAlumn': prevAlumn,
    }
    return render(request, 'delivery.html', content)

@csrf_exempt
def actualizar(request, entrega, nota, comentarioProfesor):
	delivery = get_object_or_404(Entrega, pk=entrega)
	delivery.nota = nota
	delivery.comentario_profesor = comentarioProfesor
	delivery.save()

