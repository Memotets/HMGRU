from django.http.response import HttpResponse
from django.shortcuts import render
import environ

#seguimiento particular de un nodo
from database.models.Nodos import *
from bson import ObjectId

# Create your views here.
from django.views.generic import TemplateView

def GeneralGraphView(request):
    env = environ.Env()
    environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')

    return render(request, "pages/graficaGeneral.html", {"port": env("PORT")})

def BuildingListView(request):
    env = environ.Env()
    environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')
    
    edificios = [
        env.dict('LIGEROS_I'),
        env.dict('LIGEROS_II'),
        env.dict('PESADOS_I'),
        env.dict('PESADOS_II'),
        env.dict('CAFETERIA'),
        env.dict('GOBIERNO'),
        env.dict('AULAS_I'),
        env.dict('AULAS_II')
    ]

    return render(request, "pages/listaEdificios.html", {"edificios": edificios, "port": env("PORT")})

def BuildingGraphView(request):
    # Carga del archivo .env para obtener las credenciales
    env = environ.Env()
    environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')
    #  Lista de edificios
    edificios = [
        env.dict('LIGEROS_I'),
        env.dict('LIGEROS_II'),
        env.dict('PESADOS_I'),
        env.dict('PESADOS_II'),
        env.dict('CAFETERIA'),
        env.dict('GOBIERNO'),
        env.dict('AULAS_I'),
        env.dict('AULAS_II')
    ]

    port = env("PORT")

    return render(request, "pages/graficaEdificio.html", {"edificios": edificios, "port": port})
    
def NodeGraphView(request, id):
    env = environ.Env()
    environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')
    context = {}
    print(id)
    context["port"] = env("PORT")
    context["node"] = Nodos.objects.get(_id = ObjectId(id))

    return render(request, "pages/graficaEdificios.html", context)


