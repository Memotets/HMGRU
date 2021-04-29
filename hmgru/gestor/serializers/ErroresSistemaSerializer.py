from rest_framework import serializers
from database.models.ErroresSistema import ErroresSistema

class ErroresSistemaSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'gestor'
        model = ErroresSistema
        fields = ['codigo', 'mensaje', 'moduloOrigen']
