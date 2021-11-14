from rest_framework import serializers

from database.serializers.ObjecIdFieldSerializer import ObjectIdField
from database.models.Reportes import Reporte

class ReportesSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)

    class Meta:
        app_label = 'database'
        model = Reporte
        fields = '__all__'