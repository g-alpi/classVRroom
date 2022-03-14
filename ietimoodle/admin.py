from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import ugettext_lazy as _

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = (
      (None, {'fields': ('correo', 'password', )}),
      (_('Información Personal'), {'fields': ('first_name', 'last_name')}),
      (_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                     'groups', 'user_permissions')}),
      (_('Datos Relevantes'), {'fields': ('last_login', 'date_joined')}),
        (_('Información Usuario'), {'fields': ('centro', 'privacidad')}),
    )
    add_fieldsets = (
      (None, {
          'classes': ('wide', ),
          'fields': ('nombre','correo', 'password1', 'password2'),
      }),
    )
    list_display = ['correo', 'first_name', 'last_name', 'is_staff']
    search_fields = ('correo', 'first_name', 'last_name')
    ordering = ('correo', )

admin.site.register(Centro) 
admin.site.register(Curso)
admin.site.register(Ejercicio)
admin.site.register(NivelPrivacidad) 
admin.site.register(User, UserAdmin)
admin.site.register(Entrega) 
admin.site.register(Suscripcion)
admin.site.register(Recurso)
