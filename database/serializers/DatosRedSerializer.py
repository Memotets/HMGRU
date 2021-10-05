from rest_framework import serializers
from database.models.DatosRed import DatosRed

class DatosRedSerializer(serializers.ModelSerializer):

    def create(self, validated_data):

        return DatosRed.objects.create(**validated_data)

    def is_valid(self, raise_exception=False):
        ret = super(DatosRedSerializer, self).is_valid(False)
        if self._errors:
            print("Serialization failed due to {}".format(self.errors))
            #if raise_exception:
            #    raise ValidationError(self.errors)
        return ret
        
    class Meta:
        app_label = 'database'
        model = DatosRed
        fields = ['tipo', 'entrada', 'salida', 'edificio', 'nodo', 'createdAt']
        