from django.contrib import admin
from django.urls import path

from gestor.views.DatosRedView import Datos_Red_nodo, DatosRed_general_view, DatosRed_lista_nodos
from gestor.views.NodosView import toggle_view, Prueba
from gestor.views.ErroresSistemaView import ErroresSistemaView

urlpatterns = [
    path('DatosRed/', DatosRed_general_view),
    path('nodos/lista/', DatosRed_lista_nodos),
    path('nodos/toggle/', toggle_view),
    path('nodos/individual/', Datos_Red_nodo),
    path('ErroresSistema/', ErroresSistemaView.as_view()),
    path('nodos/prueba/', Prueba),
]