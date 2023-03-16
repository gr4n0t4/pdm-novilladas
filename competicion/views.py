from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Resultado, Competicion

def tabla(request, comp_id):
    competicion = get_object_or_404(Competicion, pk=comp_id)
    resultados = Resultado.objects.filter(competicion=competicion).order_by('pub_date')
    context = {'resultados': resultados, 'entrenadores' : competicion.tabla, 'competicion': competicion.nombre }
    return render(request, 'competicions/tabla.html', context)

def index(request):
    competiciones = Competicion.objects.filter(oculta=False).order_by('nombre')
    context = {'competiciones': competiciones}
    return render(request, 'competicions/index.html', context)
