from django.contrib import admin
from django.urls import path

from gestor.views.DatosRedView import DatosRedView
from gestor.views.ErroresSistemaView import ErroresSistemaView

urlpatterns = [
    path('DatosRed/', DatosRedView.as_view()),
    path('ErroresSistema/', ErroresSistemaView.as_view()),
]