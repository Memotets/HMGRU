from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class GeneralGraphView(TemplateView):
    template_name = "pages/graficaGeneral.html"