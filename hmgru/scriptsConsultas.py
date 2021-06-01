from urllib import request, parse
import ast
import time

def consultaGeneral(previos):
    '''
     El hilo que maneja las consultas inicia antes que el servior, por lo que es necesario poner un try-excetp
     que asegure las consultas no se dentengan antes de iniciar el sistema
    '''
    try:

        # Diccionario de datos que se enviarán en la consult http
        datos = {
            'ip': '148.204.142.252',
            'octetos_previos': previos,
        }

        # Codificación de los datos para su envío
        datos = parse.urlencode(datos).encode()

        # Creaci+on de la consulta http, es importante terminar con el '/' si se enviará por método POST
        # Asignar un valor a 'data' hace que la consulta sea por POST y en lugar de GET
        req = request.Request('http://148.204.142.162:3032/gestor/DatosRed/', data = datos)

        # Envío de la consulta y procesamiento de la respuesta
        res = request.urlopen(req).read() # Lectura de la respuesta
        dec = res.decode('UTF-8') # Decodificacion de la respuesta como bytes
        lectura = ast.literal_eval(dec) # Convercion de la respuesta de bytes a diccionario
        
        return lectura
    except Exception as e:
        print(e)
        time.sleep(1)