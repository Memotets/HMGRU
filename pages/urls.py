from django.contrib import admin
from django.urls import path
from pages.views import GeneralGraphView
from pages.views import BuildingGraphView
#from pages.APIViews.datoGeneralView import DatosGeneralView

urlpatterns = [
    path('grafica/general/', GeneralGraphView, name="grafica.general"),
    path('grafica/edificios/', BuildingGraphView, name="grafica.edificios"),
]