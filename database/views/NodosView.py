from rest_framework.views import APIView
from rest_framework.response import Response

from database.models.Nodos import Nodos
from database.serializers.NodosSerializaer import NodosSerializer

class NodosView(APIView):

    def get(self, request):
        # Obtencion de los parametros por el metodo GET
        data = request.query_params

        # Separacion de los parametros GET del ip del edificio a consultar
        ip = data['ip']

        # Consulta a la base de datos para obtener el oid y idPuerrot de cada nodo del edificio consultado
        # la consulta regresa una lista de diccionarios con el formato
            # {
            #   'oid': <oid del nodo>,
            #   'idPuerto' <idPuerto del nodo>
            # }
        nodos_query = Nodos.objects.filter(edificio={'ip' : ip}).order_by('oid')
        nodos = NodosSerializer(nodos_query, many = True)

        # Diccionario para reestructrar la presentacion de los datos
        ids = {}
        
        # Reestructuracion de los datos para tener un diccionario con el formato
            # clave = oid
            # valor = (mongo_oid, idPuerto)
        for nodo in nodos.data:
            # Ejemplo de registro:
            # {'4': ('sc1684evsv11638ev21z', 'fe.1.4')}
            ids[nodo['oid']] = (nodo['_id'] ,nodo['idPuerto'])

        response = {
            'nodos': nodos.data,
            'ids': ids
        }

        return Response(response)

