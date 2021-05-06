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
        previos = int(data['octetos_previos'])
        nuevos = self.snmp(ip)

        if previos == 0:
            return Response(nuevos)

        return Response()

    def snmp(self, ip):
        # Variable donde se almacenará la suma de los octetos de los edificios
        suma_octetos_entrada = 0

        # Obteniendo el usuairo y la contraseña desde el .env
        usuario = self.Meta.env('SNMP_USER')
        clave = self.Meta.env('SNMP_PASS')

        # Comando snmp para los octetos de entrada en la ip definida
        snmp_entrada = "snmpwalk -v3 -l authPriv -u %s -a MD5 -A %s -X %s %s .1.3.6.1.2.1.2.2.1.10" %(usuario, clave, clave, ip)
        snmp_entrada = "snmpwalk -v3 -l authPriv -u %s -a MD5 -A %s -X %s %s .1.3.6.1.2.1.2.2.1.10" %(usuario, clave, clave, ip)

        # Proceso de ejecución del comando SNMP y obtencion de salida y/o errores
        consulta_entrada = subprocess.Popen(snmp_entrada.split(), stdout=subprocess.PIPE)
        respuesta_entrada, errores_entrada = consulta_entrada.communicate()
        

        # Separamos la salida y retiramos el OID de la consutla, dejando unicamente el OID de las intefaces leidas y sus octetos leidos
        datos_entrada = salida.decode().split('iso.3.6.1.2.1.2.2.1.10')

        # Octetos de la lectura
        octetos_entrada = [
            int(datos[57].split()[3]),
            int(datos[58].split()[3]),
            int(datos[59].split()[3]),
            int(datos[60].split()[3]),
            int(datos[61].split()[3]),
            int(datos[62].split()[3]),
            int(datos[63].split()[3]),
            int(datos[64].split()[3]),
        ]
        
        # Suma de los octetos
        for lectura in octetos:
           suma_octetos_entrada += lectura

        return suma_octetos_entrada

    class Meta:
        # App a la que pertencese la clase
        app_label = 'gestor'

        # Carga del archivo .env para obtener las credenciales
        env = environ.Env()
        environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/hmgru/.env')