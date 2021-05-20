from django.contrib import admin
from django.urls import path

from database.views.DatosRedView import DatosRedView

urlpatterns = [
    path('', DatosRedView.as_view()),
    path('grafica/', DatosRedView.as_view()),
]