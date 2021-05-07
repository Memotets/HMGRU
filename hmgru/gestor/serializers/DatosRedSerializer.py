from rest_framework import serializers
from database.models.DatosRed import DatosRed

class DatosRedSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return DatosRed.objects.create(**validated_data)
        
    class Meta:
        app_label = 'gestor'
        model = DatosRed
        fields = ['tipo', 'entrada', 'salida', 'createdAt']