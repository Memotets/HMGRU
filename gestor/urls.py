from django.contrib import admin
from django.urls import path

from gestor.views.DatosRedView import DatosRed_general_view, DatosRed_lista_nodos
from gestor.views.ErroresSistemaView import ErroresSistemaView


urlpatterns = [
    path('DatosRed/', DatosRed_general_view),
    path('lista/nodos', DatosRed_lista_nodos),
    path('ErroresSistema/', ErroresSistemaView.as_view()),
]