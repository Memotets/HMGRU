from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

#class GeneralGraphView(TemplateView):
    #template_name = "pages/graficaGeneral.html"

def GeneralGraphView(request):
    return render(request, "pages/graficaGeneral.html", {})
    
def BuildingGraphView(request):
    return render(request, "pages/graficaEdificios.html", {})