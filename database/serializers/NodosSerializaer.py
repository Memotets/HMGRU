from rest_framework import serializers

from database.serializers.ObjecIdFieldSerializer import ObjectIdField
from database.models.Nodos import Nodos

class NodosSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    def update(self, instance, validated_data):
        instance.activoAdministrativo = validated_data['activoAdministrativo']
        instance.save()
        return instance

    class Meta:
        app_label = 'database'
        model = Nodos
        fields = '__all__'