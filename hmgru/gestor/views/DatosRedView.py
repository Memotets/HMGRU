from rest_framework.views import APIView
from rest_framework.response import Response

from database.models.DatosRed import DatosRed
from gestor.serializers.DatosRedSerializer import DatosRedSerializer

class DatosRedView(APIView):

    def get(self, request):
        datos = DatosRed.objects.all()
        datos_serializer = DatosRedSerializer(datos, many = True)
        return Response(datos_serializer.data)

    def post(self, request):
        print("entrando en POST")
        return Response()

    class Meta:
        aoo_label = 'gestor'