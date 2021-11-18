from django.http.response import HttpResponse
from django.shortcuts import render, redirect
import environ

#seguimiento particular de un nodo
from database.models.Nodos import *
from bson import ObjectId

# Create your views here.
from django.views.generic import TemplateView

env = environ.Env()
environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')
port = env("PORT")
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


def index(request):
    return redirect('login.hmgru')

def logInView(request):
    return render(request, "pages/logIn.html", {"port" :port})

def GeneralGraphView(request):
    return render(request, "pages/graficaGeneral.html", {"port" :port})

def BuildingListView(request):
    return render(request, "pages/listaEdificios.html", {"edificios": edificios, "port": port})

def BuildingGraphView(request):
    return render(request, "pages/graficaEdificio.html", {"edificios": edificios, "port": port})
    
def NodeGraphView(request, id):
    context = {}
    context["port"]         = port
    context["node"]         = Nodos.objects.get(_id = ObjectId(id))
    context["id"]           = id
    context["edificios"]    = edificios
    return render(request, "pages/graficaNodo.html", context)

def ReportGenerator(request):
    return render(request, "pages/generarReporte.html", {"edificios": edificios, "port": port})

