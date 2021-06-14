from database.models.Edificio import Edificio
from rest_framework.views import APIView
from rest_framework.response import Response

from database.models.DatosRed import DatosRed
from database.serializers.DatosRedSerializer import DatosRedSerializer

class DatosRedView(APIView):

    def get(self, request):
        data = request.query_params
        print(data)
        datos = None
        datos_serializer = None

        try:
            datos
            tip = int(data['tipo'])
            print(tip)
            if tip == 0:
                print("tipo 0")
                datos = DatosRed.objects.filter(tipo=0).last()
            elif tip == 1:
                datos = DatosRed.objects.filter(tipo=1, edificio={'ip': data['ip']}).last()

            print(datos)
            datos_serializer = DatosRedSerializer(datos)
        except Exception as ex:
            print(ex)
            datos = DatosRed.objects.all()
            datos_serializer = DatosRedSerializer(datos, many = True)
        
        return Response(datos_serializer.data)