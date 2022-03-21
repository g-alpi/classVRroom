from django.shortcuts import render,  get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

# Create your views here.
from django.http import HttpResponse
from .forms import LoginForm
from .models import *




class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'


@login_required
def index(request, exerciseid, alumnid):
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
    return render(request, 'index.html', content)