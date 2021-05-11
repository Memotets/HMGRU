from rest_framework.views import APIView
from rest_framework.response import Response

from database.models.ErroresSistema import ErroresSistema
from gestor.serializers.ErroresSistemaSerializer import ErroresSistemaSerializer

class ErroresSistemaView(APIView):

    def get(self, request):
        errores = ErroresSistema.objects.all()
        errores_serializer = ErroresSistemaSerializer(errores, many = True)
        return Response(errores_serializer.data)

    class Meta:
        aoo_label = 'gestor'