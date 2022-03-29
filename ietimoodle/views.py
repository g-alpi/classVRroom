import re
from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse

from .models import *
import os, mimetypes

class MyAuthForm(AuthenticationForm):
	error_messages = {
		'invalid_login': _(
			"Asegurate de introducir el correo y la contraseña correctamente."
			" Ten en cuenta las máyusculas."
		),
		'inactive': _("El ususario no esta activo"),
	}


class LoginView(auth_views.LoginView):
	form_class = LoginForm
	authentication_form = MyAuthForm
	template_name = 'registration/login.html'

def home(request):
	return render(request, 'home.html')

def logout_view(request):
	logout(request)
	return render(request, "logout.html")

@login_required
def download(request, element, filename=''):
	if filename != '':
		try:
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			filepath = BASE_DIR + '/archivos/' + element + '/' + filename
			path = open(filepath, 'rb')
			mime_type, _ = mimetypes.guess_type(filepath)
			response = HttpResponse(path, content_type=mime_type)
			response['Content-Disposition'] = "attachment; filename=%s" % filename
			return response
		except FileNotFoundError:
			return HttpResponseNotFound('Error 404 File not found')
	else:
		return render(request, 'file.html')

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
def grade(request, cursoid):
    recursos = Recurso.objects.filter(curso=cursoid)
    ejercicios = Ejercicio.objects.filter(curso=cursoid)
    role= Suscripcion.objects.filter(curso=cursoid, user=request.user.pk)[0]
    suscripciones=Suscripcion.objects.filter(curso=cursoid)[0]
    firstAlId=get_object_or_404(User, pk=suscripciones.user.pk)
    content= {
        'resources': recursos,
        'exercises': ejercicios,
        'role': role,
        'grade': get_object_or_404(Curso, pk=cursoid),
        'firstal': firstAlId
    }
    return render(request, 'grade.html', content)

@login_required
def qualifications(request, cursoid):
    alumn=get_object_or_404(User, pk=request.user.pk)
    ejercicios = Ejercicio.objects.filter(curso=cursoid)
    deliveries=Entrega.objects.filter(user=alumn.pk, curso=cursoid)
    deliveriesRealizadas=[]
    for d in deliveries:
        deliveriesRealizadas.append(d.ejercicio.pk)
    content= {
        'grade': get_object_or_404(Curso, pk=cursoid),
        'alumn': alumn,
        'exercises': ejercicios,
        'deliveries': deliveries,
        'deliveriesRealizadas': deliveriesRealizadas
    }
    return render(request, 'qualifications.html', content)

@login_required
def resource(request, resourceid):
	resource=get_object_or_404(Recurso, pk=resourceid)
	curso=get_object_or_404(Curso, pk=resource.curso.pk)
	content= {
		'resource': resource,
		'curso': curso
	}
	return render(request, 'resource.html', content)

@login_required
def exercise(request, exerciseid):
	exercise=get_object_or_404(Ejercicio, pk=exerciseid)
	curso=get_object_or_404(Curso, pk=exercise.curso.pk)
	user=get_object_or_404(User, pk=request.user.pk)
	print(user)

	entrega=Entrega.objects.filter(ejercicio=exerciseid, user=user.pk)
	print(entrega)
	content= {
		'exercise': exercise,
		'curso': curso,
		'entrega': entrega
	}
	return render(request, 'exercise.html', content)

@login_required
def delivery(request, exerciseid, alumnid):
    alumn= get_object_or_404(User, pk=alumnid)
    exercise=get_object_or_404(Ejercicio, pk=exerciseid)
    try:
        alumnos= Entrega.objects.filter(ejercicio=exercise)
        curso=get_object_or_404(Curso, pk=exercise.curso.pk)
        delivery=Entrega.objects.filter(ejercicio=exercise, user=alumn)[0]
        alumnosID=[]
        for i in alumnos :
            alumnosID.append(i.user.pk)

        if alumnosID.index(alumnid) == len(alumnosID)-1:
            nextAlumn = alumnosID[0]
        else:
            nextAlumn = alumnosID[alumnosID.index(alumnid) + 1]

        prevAlumn = alumnosID[alumnosID.index(alumnid) - 1]
    except:
        delivery=""
        prevAlumn=""
        nextAlumn=""
    
    
    content = {
        'alumn': alumn,
        'exercise': exercise,
        'delivery': delivery,
        'nextAlumn': nextAlumn,
        'prevAlumn': prevAlumn,
        'curso': curso
    }
    return render(request, 'delivery.html', content)


@login_required
def fastcorrection(request, exerciseid):
    exercise=get_object_or_404(Ejercicio, pk=exerciseid)
    curso=get_object_or_404(Curso, nombre=exercise.curso)
    deliveries=Entrega.objects.filter(ejercicio=exercise)
    alumnos= Suscripcion.objects.filter(curso=curso.pk, tipo="alumno")
    curso=get_object_or_404(Curso, pk=exercise.curso.pk)
    alumnosEntregado=[]
    for d in deliveries:
        alumnosEntregado.append(d.user.pk)
    
    content = {
        'alumnos': alumnos,
        'exercise': exercise,
        'deliveries': deliveries,
        'alumnosEntregado': alumnosEntregado,
        'curso': curso
    }
    return render(request, 'fastcorrection.html', content)

@csrf_exempt
def actualizar(request, entrega, nota, comentarioProfesor,estadoEntrega):
	if estadoEntrega==1:
		estadoEntrega=True
	else:
		estadoEntrega=False
	delivery = get_object_or_404(Entrega, pk=entrega)
	delivery.cualificacion = nota
	delivery.estado = estadoEntrega
	delivery.comentario_profesor = comentarioProfesor
	delivery.save()

