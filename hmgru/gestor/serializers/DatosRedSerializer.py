from rest_framework import serializers
from database.models.DatosRed import DatosRed

class DatosRedSerializer(serializers.ModelSerializer):
    class Meta:
        app_label = 'gestor'
        model = DatosRed
        fields = ['tipo', 'entrada', 'salida', 'createdAt']