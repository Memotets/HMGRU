from rest_framework.views import APIView
from rest_framework.response import Response

from database.models.DatosRed import DatosRed
from gestor.serializers.DatosRedSerializer import DatosRedSerializer

import environ
import subprocess

class DatosRedView(APIView):

    def get(self, request):
        datos = DatosRed.objects.all()
        datos_serializer = DatosRedSerializer(datos, many = True)
        return Response(datos_serializer.data)

    def post(self, request):
        data = request.data

        ip = data['ip']
        previos = dict(data['octetos_previos'])

        #previos_entrada = int(previos['entrada'])
        #previos_salida = int(previos['salida'])

        nuevos = self.snmp(ip)
        
        respuesta = {
            'octetos_entrada': nuevos[0],
            'octetos_salida': nuevos[1]
        }

        #if previos_entrada == 0:
         #   print(Treu)
            #return Response(respuesta)

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