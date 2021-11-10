from database.views.NodosView import NodosView
from django.contrib import admin
from django.urls import path

from database.views.DatosRedView import grafica_datos
from database.views.Reportes import reportar, datos_reporte

urlpatterns = [
    path('grafica/', grafica_datos),
    path('reporte/generar/', datos_reporte),
    path('reporte/consultar/', reportar),
    path('lista/nodos/', NodosView.as_view()),
]