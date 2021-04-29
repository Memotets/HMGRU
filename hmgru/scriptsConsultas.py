from urllib import request, parse

def consultaGeneral():
    '''
     El hilo que maneja las consultas inicia antes que el servior, por lo que es necesario poner un try-excetp
     que asegure las consultas no se dentengan antes de iniciar el sistema
    '''
    try:
        # Diccionario de datos que se enviarán en la consult http
        datos = {
            'ip': '148.204.142.252'
        }

        # Codificación de los datos para su envío
        datos = parse.urlencode(datos).encode()

        # Creaci+on de la consulta http, es importante terminar con el '/' si se enviará por método POST
        # Asignar un valor a 'data' hace que la consulta sea por POST y en lugar de GET
        req = request.Request('http://148.204.142.162:3031/gestor/DatosRed/', data = datos)

        # Envío de la consulta, si es necesario la respuesta se puede asiganr en una variable
        request.urlopen(req)
    except Exception as e:
        print(e)