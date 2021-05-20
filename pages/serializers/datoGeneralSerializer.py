"""Wop"""
from rest_framework import serializers
from database.models.DatosRed import DatosRed

class DatoGeneralSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return DatosRed.objects.create(**validated_data)
        
    class Meta:
        app_label = 'APIWeb'
        model = DatosRed
        fields = ['tipo', 'entrada', 'salida', 'createdAt']