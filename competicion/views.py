from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Resultado, Entrenador, Competicion
import math
from django.urls import resolve
   

def tabla(request, comp_id):
    competicion = get_object_or_404(Competicion, pk=comp_id)

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
        if resultado.td_casa == resultado.td_fuera:
            entrenadores[resultado.entrenador_casa.id]['empates'] += 1
            entrenadores[resultado.entrenador_fuera.id]['empates'] += 1

            entrenadores[resultado.entrenador_casa.id]['elo'] -= diferencia
            entrenadores[resultado.entrenador_fuera.id]['elo'] += diferencia

        elif resultado.td_casa > resultado.td_fuera:
            entrenadores[resultado.entrenador_casa.id]['victorias'] += 1
            entrenadores[resultado.entrenador_fuera.id]['derrotas'] += 1

            entrenadores[resultado.entrenador_casa.id]['elo'] += 20 - diferencia
            entrenadores[resultado.entrenador_fuera.id]['elo'] -= 20 + diferencia
        else:
            entrenadores[resultado.entrenador_casa.id]['derrotas'] += 1
            entrenadores[resultado.entrenador_fuera.id]['victorias'] += 1

            entrenadores[resultado.entrenador_casa.id]['elo'] -= 20 + diferencia
            entrenadores[resultado.entrenador_fuera.id]['elo'] += 20 - diferencia
    entrenadores_lista = []
    for value in entrenadores.values():
        if value['total'] > 9:
            value['clase'] = 'clasificado'
        if value['total'] > 0:
            entrenadores_lista.append(value)

    context = {'resultados': resultados, 'entrenadores' : sorted(entrenadores_lista, key=lambda x: x.get('elo'), reverse=True)}
    return render(request, 'competicions/tabla.html', context)

def index(request):
    competiciones = Competicion.objects.order_by('pub_date')
    context = {'competiciones': competiciones}
    return render(request, 'competicions/index.html', context)