from django.http import HttpResponse

from urllib import request as url_request
from urllib import parse

import subprocess

def pruebas(request):

    datos = {
        'ip': '148.204.142.252',
        'octetos_previos': 0,
    }

    # Codificación de los datos para su envío
    datos = parse.urlencode(datos).encode()

    # Creaci+on de la consulta http, es importante terminar con el '/' si se enviará por método POST
    # Asignar un valor a 'data' hace que la consulta sea por POST y en lugar de GET
    req = url_request.Request('http://148.204.142.162:3031/gestor/DatosRed/', data = datos)

    # Envío de la consulta, si es necesario la respuesta se puede asiganr en una variable
    retorno = url_request.urlopen(req)

    return HttpResponse(retorno)