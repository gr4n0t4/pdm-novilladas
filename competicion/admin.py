from django.contrib import admin

from .models import Competicion, Entrenador, Resultado

admin.site.register(Competicion)
admin.site.register(Entrenador)
admin.site.register(Resultado)