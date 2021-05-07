from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime

from database.models.DatosRed import DatosRed
from gestor.serializers.DatosRedSerializer import DatosRedSerializer

import environ
import subprocess
import ast

class DatosRedView(APIView):

    def get(self, request):
        datos = DatosRed.objects.all()
        datos_serializer = DatosRedSerializer(datos, many = True)
        return Response(datos_serializer.data)

    def post(self, request):
        data = request.data

        ip = data['ip']
        previos = ast.literal_eval(data['octetos_previos'])

        previos_entrada = 0 if (previos is None) else int(previos['entrada'])
        previos_salida =  0 if (previos is None) else int(previos['entrada'])

        nuevos = self.snmp(ip)
        
        respuesta = {
            'entrada': int(nuevos[0]),
            'salida': int(nuevos[1])
        }

        if previos_entrada != 0:
            Bps_entrada = ((respuesta['entrada'] - int(previos_entrada)) * 8) / (float(self.Meta().env('TIMELAPSE')) * 1000)
            Bps_salida = ((respuesta['salida'] - int(previos_salida)) * 8) / (float(self.Meta().env('TIMELAPSE')) * 1000)

            Mbps_entrada = Bps_entrada / 1024 / 1000
            Mbps_salida = Bps_salida / 1024 / 1000

            if Mbps_entrada < 0:
                Mbps_entrada = -Mbps_entrada

            if Mbps_salida < 0:
                Mbps_salida = -Mbps_salida

            timestamp = datetime.now()
            datos = {
                'tipo': 0,
                'entrada': Mbps_entrada,
                'salida': Mbps_salida,
                'createdAt': timestamp
            }

            serializador_datos_red = DatosRedSerializer(data = datos)
            if serializador_datos_red.is_valid():
                datos_red = serializador_datos_red.save()
                print(datos_red)

        #print(respuesta)
        return Response(respuesta)

    def snmp(self, ip):
        # Variables donde se almacenará la suma de los octetos de entrada y salida de los edificios
        suma_octetos_entrada = 0
        suma_octetos_salida = 0

        # Obteniendo el usuairo y la contraseña desde el .env
        usuario = self.Meta.env('SNMP_USER')
        clave = self.Meta.env('SNMP_PASS')

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
        datos_entrada = respuesta_entrada.decode().split('iso.3.6.1.2.1.2.2.1.10')
        datos_salida = respuesta_salida.decode().split('iso.3.6.1.2.1.2.2.1.16')

        # Octetos de la lectura de entrada
        octetos_entrada = [
            int(datos_entrada[57].split()[3]),
            int(datos_entrada[58].split()[3]),
            int(datos_entrada[59].split()[3]),
            int(datos_entrada[60].split()[3]),
            int(datos_entrada[61].split()[3]),
            int(datos_entrada[62].split()[3]),
            int(datos_entrada[63].split()[3]),
            int(datos_entrada[64].split()[3]),
        ]

        # Octetos de la lectura de salida
        octetos_salida = [
            int(datos_salida[57].split()[3]),
            int(datos_salida[58].split()[3]),
            int(datos_salida[59].split()[3]),
            int(datos_salida[60].split()[3]),
            int(datos_salida[61].split()[3]),
            int(datos_salida[62].split()[3]),
            int(datos_salida[63].split()[3]),
            int(datos_salida[64].split()[3]),
        ]
        
        # Suma de los octetos de entrada
        for octetos in octetos_entrada:
           suma_octetos_entrada += octetos

        for octetos in octetos_salida:
            suma_octetos_salida += octetos

        return (suma_octetos_entrada, suma_octetos_salida)

    class Meta:
        # App a la que pertencese la clase
        app_label = 'gestor'

        # Carga del archivo .env para obtener las credenciales
        env = environ.Env()
        environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/hmgru/.env')