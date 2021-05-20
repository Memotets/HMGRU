from rest_framework.views import APIView
from rest_framework.response import Response

from database.models.DatosRed import DatosRed
from database.serializers.DatosRedSerializer import DatosRedSerializer

class DatosRedView(APIView):

    def get(self, request):
        data = request.query_params
        datos = None
        datos_serializer = None

        try:
            #datos = DatosRed.objects.filter(tipo = data['tipo'])
            datos = DatosRed.objects.last()
            datos_serializer = DatosRedSerializer(datos)
        except Exception as ex:
            print(ex)
            datos = DatosRed.objects.all()
            datos_serializer = DatosRedSerializer(datos, many = True)
        
        return Response(datos_serializer.data)