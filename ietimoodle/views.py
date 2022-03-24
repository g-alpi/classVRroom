import re
from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

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
    delivery=Entrega.objects.filter(ejercicio=exercise.pk, user=alumn)[0]
    nextAlumn=alumnid+1
    prevAlumn=alumnid-1
    content = {
        'alumn': alumn,
        'exercise': exercise,
        'delivery': delivery,
        'nextAlumn': nextAlumn,
        'prevAlumn': prevAlumn,
    }
    return render(request, 'delivery.html', content)