from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime

from database.models.DatosRed import DatosRed
from database.serializers.DatosRedSerializer import DatosRedSerializer

import environ
import subprocess
import ast

@api_view(['POST'])
def DatosRed_general_view(request):
    
    if(request.method == 'POST'):
        data = request.data

        ip = data['ip']
        previos = ast.literal_eval(data['octetos_previos'])

        previos_entrada = 0 if (previos is None) else int(previos['entrada'])
        previos_salida =  0 if (previos is None) else int(previos['salida'])

        previos_entrada_edificio = 0 if (previos is None) else previos['edificios_entrada']
        previos_salida_edificio =  0 if (previos is None) else previos['edificios_salida']

        datos_entrada, datos_salida = snmp(ip)

        nuevos_entrada: int = 0
        nuevos_salida: int = 0

        octetos_entrada = []
        octetos_salida = []
        for i in range(57, 65):
            entrada = int(datos_entrada[i].split()[3])
            salida = int(datos_salida[i].split()[3])

            octetos_entrada.append(entrada)
            octetos_salida.append(salida)
            
            nuevos_entrada += entrada
            nuevos_salida += salida

        if previos_entrada != 0 and previos_salida != 0 and previos_entrada_edificio != 0 and previos_salida_edificio != 0:
            guardarConsulta((nuevos_entrada - int(previos_entrada)), (nuevos_salida - int(previos_salida)), 0)  

            edificios = Meta.edificios

            for i in range(0, 8):
                edificio = edificios[i]

                dif_entrada: int = octetos_entrada[i] - int(previos_entrada_edificio[i])
                dif_salida: int = octetos_salida[i] - int(previos_salida_edificio[i])

                guardarConsulta(dif_entrada, dif_salida, 1, edificio=edificio)

        response = {
            'entrada': nuevos_entrada,
            'salida': nuevos_salida,
            'edificios_entrada':  octetos_entrada,
            'edificios_salida': octetos_salida
        }
        #print(respuesta)

        return Response(response)

@api_view(['POST'])
def DatosRed_lista_nodos(request):

    if(request.method == 'POST'):
        data = request.data

        ip = data['ip']
        oids = data['oids']
        previos = ast.literal_eval(data['previos'])

        previos_entrada = 0 if (previos is None) else int(previos['entrada'])
        previos_salida =  0 if (previos is None) else int(previos['salida'])

        octetos_entrada = []
        octetos_salida = []
        _ids = []

        consumo_entrada = []
        consumo_salida = []

        datos_entrada, datos_salida = snmp(ip)

        limit = len(datos_entrada)
        for i in range(0, limit):
            key = '%i' %(i)

            if key in oids:
                entrada = int(datos_entrada[i].split()[3])
                salida = int(datos_salida[i].split()[3])

                octetos_entrada.append(entrada)
                octetos_salida.append(salida)
                _ids.append(oids[key][0])

        if previos_entrada != 0:
            for i in range(0, len(previos_entrada)):
                dif_entrada: int = octetos_salida[i] - previos_entrada[i]
                dif_salida: int = octetos_salida[i] - previos_salida[i]

                Mbps_entrada, Mbps_salida = guardarConsulta(dif_entrada, dif_salida, nodo=_ids[i])

                consumo_entrada.append(Mbps_entrada)
                consumo_salida.append(Mbps_salida)
        else:
            for i in range(0, len(previos_entrada)):
                consumo_entrada.append(0)
                consumo_salida.append(0)

        response = {
            'octetos_entrada': octetos_entrada,
            'octetos_salida': octetos_salida,
            'consumo_entrada': consumo_entrada,
            'consumo_salida': consumo_salida
        }

        return Response(response)
        

def snmp(ip):
    # Obteniendo el usuairo y la contraseña desde el .env
    usuario = Meta.env('SNMP_USER')
    clave = Meta.env('SNMP_PASS')

    # Comandos snmp para los octetos en la ip definida
    snmp_entrada = "snmpwalk -v3 -l authPriv -u %s -a MD5 -A %s -X %s %s .1.3.6.1.2.1.2.2.1.10" %(usuario, clave, clave, ip) # Octetos de entrada
    snmp_salida = "snmpwalk -v3 -l authPriv -u %s -a MD5 -A %s -X %s %s .1.3.6.1.2.1.2.2.1.16" %(usuario, clave, clave, ip) # Octetos de salida

    # Proceso de ejecución de los comandos SNMP
    consulta_entrada = subprocess.Popen(snmp_entrada.split(), stdout=subprocess.PIPE)
    consulta_salida = subprocess.Popen(snmp_salida.split(), stdout=subprocess.PIPE)

    # Obtencion de la respuesta y/o errores de la ejecucion de los comandos
    respuesta_entrada, errores_entrada = consulta_entrada.communicate()
    respuesta_salida, errores_salida = consulta_salida.communicate()

    # Separamos la salida y retiramos el OID de la consutla, dejando unicamente el OID de las intefaces leidas y sus octetos leidos
    datos_entrada = respuesta_entrada.decode().split('iso.3.6.1.2.1.2.2.1.10') #.123 ext 32 1235167813
    datos_salida = respuesta_salida.decode().split('iso.3.6.1.2.1.2.2.1.16')

    return datos_entrada, datos_salida

def guardarConsulta(dif_entrada, dif_salida, tipo, edificio=None, nodo=None): 
    Bps_entrada = (dif_entrada * 8) / (Meta.env.float('TIMELAPSE') * 1000)
    Bps_salida = (dif_salida * 8) / (Meta.env.float('TIMELAPSE') * 1000)

    Mbps_entrada = Bps_entrada / 1024 / 1000
    Mbps_salida = Bps_salida / 1024 / 1000

    if Mbps_entrada < 0:
        Mbps_entrada = -Mbps_entrada

    if Mbps_salida < 0:
        Mbps_salida = -Mbps_salida

    timestamp = datetime.now()
    datos = {
        'tipo': tipo,
        'entrada': Mbps_entrada,
        'salida': Mbps_salida,
        'createdAt': timestamp
    }

    if edificio is not None:
        datos['edificio'] = edificio

    if nodo is not None:
        datos['nodo'] = nodo

    serializador_datos_red = DatosRedSerializer(data = datos)
    if serializador_datos_red.is_valid():
        datos_red = serializador_datos_red.save()

        return Mbps_entrada, Mbps_salida
    else:
        print("Data not valid")
        return 0, 0

class Meta:
    # App a la que pertencese la clase
    app_label = 'gestor'

    # Carga del archivo .env para obtener las credenciales
    env = environ.Env()
    environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')

    edificios = [
        env.dict('LIGEROS_I'),
        env.dict('LIGEROS_II'),
        env.dict('PESADOS_II'),
        env.dict('PESADOS_I'),
        env.dict('CAFETERIA'),
        env.dict('GOBIERNO'),
        env.dict('AULAS_I'),
        env.dict('AULAS_II'),
    ]
