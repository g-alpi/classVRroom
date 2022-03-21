import re
from django.shortcuts import render,  get_object_or_404

# Create your views here.
from django.http import HttpResponse

from .models import *

def home(request):
    return render(request, 'home.html')

def dashboard(request, userid):
    suscripciones=Suscripcion.objects.filter(user=userid)
    user= get_object_or_404(User, pk=userid)
    content={
        'user': user,
        'suscripciones': suscripciones,
    }
    return render(request, 'dashboard.html', content)

def curso(request, cursoid):
    return render(request, 'curso.html')

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