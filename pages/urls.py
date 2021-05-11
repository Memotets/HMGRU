from django.contrib import admin
from django.urls import path, include
from pages.views import GeneralGraphView

urlpatterns = [
    #path('', GeneralGraphView.as_view()),
    path('', GeneralGraphView)
]