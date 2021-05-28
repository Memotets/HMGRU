from django.contrib import admin
from django.urls import path
from pages.views import GeneralGraphView
#from pages.APIViews.datoGeneralView import DatosGeneralView

urlpatterns = [
    path('', GeneralGraphView),
    #path('APIweb/', DatosGeneralView.as_view()),
]