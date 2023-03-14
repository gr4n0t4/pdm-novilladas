from django.contrib import admin

from .models import Competicion, Entrenador, Resultado


class EntrenadorAdmin(admin.ModelAdmin):
    ordering = ['nombre']
class CompeticionAdmin(admin.ModelAdmin):
    ordering = ['-pub_date']

admin.site.register(Competicion, CompeticionAdmin)
admin.site.register(Entrenador, EntrenadorAdmin)
admin.site.register(Resultado)