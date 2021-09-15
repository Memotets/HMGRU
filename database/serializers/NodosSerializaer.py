from django.utils.encoding import smart_text
from rest_framework import serializers
from database.models.Nodos import Nodos

from bson import ObjectId
from bson.errors import InvalidId


class ObjectIdField(serializers.Field):
    def to_internal_value(self, data):

        try:
            return ObjectId(str(data))
        except InvalidId:
            raise serializers.ValidationError(
                '`{}` is not a valid ObjectID'.format(data)
            )
        
    def to_representation(self, value):
        if not ObjectId.is_valid(value):
            raise InvalidId

        return smart_text(value)

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