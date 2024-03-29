from django.contrib import admin
from django.urls import path
from pages.views import *

#from pages.APIViews.datoGeneralView import DatosGeneralView
#from pages.prueba import *

urlpatterns = [
    path('', index),
    #path("login/", logInView, name="login.hmgru"),
    path('grafica/general/', GeneralGraphView, name="grafica.general"),
    path('grafica/edificios/', BuildingGraphView, name="grafica.edificios"),
    path('lista/edificios/', BuildingListView, name="lista.edificios"),
    path('grafica/nodo/<id>', NodeGraphView, name="grafica.nodo"),
    path('reporte/general', ReportGenerator, name = 'reportes.generales')
    #path('lista/prueba/', Prueba, name="lista.edificiosx")
    # 613f97cdb99f346542f3277f , fe.1.20
    #
]