from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
import math
class Competicion(models.Model):
    nombre = models.CharField(max_length=200)
    tabla = models.JSONField(default=[])
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.nombre

class Entrenador(models.Model):
    nombre = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre

class Resultado(models.Model):
    entrenador_casa = models.ForeignKey(Entrenador, on_delete=models.CASCADE, related_name='casa')
    entrenador_fuera = models.ForeignKey(Entrenador, on_delete=models.CASCADE, related_name='fuera')
    td_casa= models.IntegerField(default=0)
    td_fuera= models.IntegerField(default=0)
    competicion = models.ForeignKey(Competicion, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return f'{self.entrenador_casa} vs {self.entrenador_fuera.nombre} ({self.td_casa}-{self.td_fuera})'
    
@receiver(post_delete, sender=Resultado)
def update_table_delete(sender, instance, using, **kwargs):
    update_table(instance.competicion)
@receiver(post_save, sender=Resultado)
def update_table_save(sender, instance, using, **kwargs):
    update_table(instance.competicion)    


def update_table(competicion):
    print ('Update table')
    resultados = Resultado.objects.filter(competicion=competicion).order_by('pub_date')
    entrenadores_obj = Entrenador.objects.order_by('nombre')

    entrenadores = {}
    for entrenador in entrenadores_obj:
        entrenadores[entrenador.id] = {'nombre': entrenador.nombre,
                                       'total': 0,
                                       'victorias': 0,
                                       'empates': 0,
                                       'derrotas': 0,
                                       'elo': 1000,
                                       'clase': ''
                                       }
                                       
    for resultado in resultados:
        entrenadores[resultado.entrenador_casa.id]['total'] += 1
        entrenadores[resultado.entrenador_fuera.id]['total'] += 1
        diferencia = entrenadores[resultado.entrenador_casa.id]['elo'] - entrenadores[resultado.entrenador_fuera.id]['elo']
        diferencia = math.trunc(diferencia/10)
        if diferencia < -10:
            diferencia = -10
        elif diferencia > 10:
            diferencia = 10
        if resultado.td_casa == resultado.td_fuera:
            entrenadores[resultado.entrenador_casa.id]['empates'] += 1
            entrenadores[resultado.entrenador_fuera.id]['empates'] += 1

            entrenadores[resultado.entrenador_casa.id]['elo'] -= diferencia
            entrenadores[resultado.entrenador_fuera.id]['elo'] += diferencia

        elif resultado.td_casa > resultado.td_fuera:
            entrenadores[resultado.entrenador_casa.id]['victorias'] += 1
            entrenadores[resultado.entrenador_fuera.id]['derrotas'] += 1

            entrenadores[resultado.entrenador_casa.id]['elo'] += 20 - diferencia
            entrenadores[resultado.entrenador_fuera.id]['elo'] -= 20 - diferencia
        else:
            entrenadores[resultado.entrenador_casa.id]['derrotas'] += 1
            entrenadores[resultado.entrenador_fuera.id]['victorias'] += 1

            entrenadores[resultado.entrenador_casa.id]['elo'] -= 20 + diferencia
            entrenadores[resultado.entrenador_fuera.id]['elo'] += 20 + diferencia
    entrenadores_lista = []
    for value in entrenadores.values():
        if value['total'] > 9:
            value['clase'] = 'clasificado'
        if value['total'] > 0:
            entrenadores_lista.append(value)

    competicion.tabla = sorted(entrenadores_lista, key=lambda x: x.get('elo'), reverse=True)
    competicion.save()