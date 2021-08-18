from django.contrib import admin
from django.urls import path
from pages.views import *

#from pages.APIViews.datoGeneralView import DatosGeneralView

urlpatterns = [
    path('grafica/general/', GeneralGraphView, name="grafica.general"),
    path('grafica/edificios/', BuildingGraphView, name="grafica.edificios"),
    path('lista/edificios/', BuildingListView, name="lista.edificios")
]