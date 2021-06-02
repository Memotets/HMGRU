from django.contrib import admin
from django.urls import path
from pages.views import GeneralGraphView
from pages.views import BuildingGraphView
#from pages.APIViews.datoGeneralView import DatosGeneralView

urlpatterns = [
    path('', GeneralGraphView),
    path('Edificios/', BuildingGraphView),
]