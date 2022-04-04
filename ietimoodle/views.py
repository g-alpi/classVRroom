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
from .serializers import * 
from rest_framework import viewsets
from django.contrib.auth.models import Permission
from rest_framework import permissions
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
	tareas = Tarea.objects.filter(curso=cursoid)
	role= Suscripcion.objects.filter(curso=cursoid, user=request.user.pk)[0]
	alumnos= Suscripcion.objects.filter(curso=cursoid,tipo='alumno')[0]
	firstAlId=get_object_or_404(User, pk=alumnos.user.pk)
	content= {
		'resources': recursos,
		'tasks': tareas,
		'role': role,
		'grade': get_object_or_404(Curso, pk=cursoid),
		'firstal': firstAlId
	}
	return render(request, 'grade.html', content)

@login_required
def qualifications(request, cursoid):
	alumn=get_object_or_404(User, pk=request.user.pk)
	tasks = Tarea.objects.filter(curso=cursoid)
	deliveries=Entrega.objects.filter(user=alumn.pk, curso=cursoid)
	qualifications=Calificacion.objects.filter(user=alumn.pk)
	deliveriesRealizadas=[]
	for d in deliveries:
		deliveriesRealizadas.append(d.tarea.pk)
	content= {
		'grade': get_object_or_404(Curso, pk=cursoid),
		'alumn': alumn,
		'tasks': tasks,
		'deliveries': deliveries,
		'qualifications': qualifications,
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
def task(request, taskid):
	tarea=get_object_or_404(Tarea, pk=taskid)
	curso=get_object_or_404(Curso, pk=tarea.curso.pk)
	alumn=get_object_or_404(User, pk=request.user.pk)
	qualification=get_object_or_404(Calificacion, user=alumn.pk, tarea=task.pk)
	tasks=Tarea.objects.filter(curso=curso.pk)
	entrega=Entrega.objects.filter(tarea=taskid, user=alumn.pk)
	content= {
		'task': tarea,
		'curso': curso,
		'entrega': entrega,
		'qualification': qualification,
		'tasks': tasks
	}
	return render(request, 'task.html', content)

@login_required
def delivery(request, taskid, alumnid):
	alumn= get_object_or_404(User, pk=alumnid)
	task=get_object_or_404(Tarea, pk=taskid)
	try:
		alumnos= Entrega.objects.filter(tarea=task)
		curso=get_object_or_404(Curso, pk=task.curso.pk)
		delivery=Entrega.objects.filter(tarea=task, user=alumn)[0]
		qualification=get_object_or_404(Calificacion, user=alumn.pk, tarea=task.pk)
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
		'task': task,
		'delivery': delivery,
		'nextAlumn': nextAlumn,
		'prevAlumn': prevAlumn,
		'qualification': qualification,
		'curso': curso
	}
	return render(request, 'delivery.html', content)


@login_required
def fastcorrection(request, taskid):
	task=get_object_or_404(Tarea, pk=taskid)
	curso=get_object_or_404(Curso, nombre=task.curso)
	deliveries=Entrega.objects.filter(task=task)
	alumnos= Suscripcion.objects.filter(curso=curso.pk, tipo="alumno")
	curso=get_object_or_404(Curso, pk=task.curso.pk)
	qualifications=Calificacion.objects.filter(tarea=task.pk)
	alumnosEntregado=[]
	for d in deliveries:
		alumnosEntregado.append(d.user.pk)
	
	content = {
		'alumnos': alumnos,
		'task': task,
		'deliveries': deliveries,
		'alumnosEntregado': alumnosEntregado,
		'qualifications': qualifications,
		'curso': curso
	}
	return render(request, 'fastcorrection.html', content)

@csrf_exempt
def actualizarEjercicioIndiviual(request, entrega, nota, comentarioProfesor,estadoEntrega):
	if estadoEntrega==1:
		estadoEntrega=True
	else:
		estadoEntrega=False
	delivery = get_object_or_404(Entrega, pk=entrega)
	delivery.cualificacion = nota
	delivery.estado = estadoEntrega
	delivery.comentario_profesor = comentarioProfesor
	delivery.save()

@csrf_exempt
def actualizar(request, entrega, nota, comentarioProfesor):
	delivery = get_object_or_404(Calificacion, pk=entrega)
	delivery.nota = nota
	delivery.comentario_profesor = comentarioProfesor
	delivery.save()
