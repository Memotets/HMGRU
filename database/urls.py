from database.views.NodosView import NodosView
from django.urls import path

from database.views.DatosRedView import grafica_datos
from database.views.Reportes import cosultar_reporte, datos_reporte

urlpatterns = [
    path('grafica/', grafica_datos),
    path('reporte/generar/', datos_reporte),
    path('reporte/consultar/', cosultar_reporte),
    path('lista/nodos/', NodosView.as_view()),
]