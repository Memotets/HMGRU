from rest_framework import serializers
from database.models.Nodos import Nodos

class NodosSerializer(serializers.ModelSerializer):
     class Meta:
        app_label = 'database'
        model = Nodos
        fields = '__all__'