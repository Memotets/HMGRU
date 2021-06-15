from django.http.response import HttpResponse
from django.shortcuts import render
import environ
# Create your views here.
from django.views.generic import TemplateView

def GeneralGraphView(request):
    return render(request, "pages/graficaGeneral.html", {})

def BuildingGraphView(request):
    # Carga del archivo .env para obtener las credenciales
    env = environ.Env()
    environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')
    #  Lista de edificios
    edificios = [
        env.dict('LIGEROS_I'),
        env.dict('LIGEROS_II'),
        env.dict('PESADOS_II'),
        env.dict('PESADOS_I'),
        env.dict('CAFETERIA'),
        env.dict('GOBIERNO'),
        env.dict('AULAS_I'),
        env.dict('AULAS_II')
    ]

    return render(request, "pages/graficaEdificio.html", {"edificios": edificios})
    

