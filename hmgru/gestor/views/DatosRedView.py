from rest_framework.views import APIView
from rest_framework.response import Response

from database.models.DatosRed import DatosRed
from gestor.serializers.DatosRedSerializer import DatosRedSerializer

import environ

class DatosRedView(APIView):

    def get(self, request):
        datos = DatosRed.objects.all()
        datos_serializer = DatosRedSerializer(datos, many = True)
        return Response(datos_serializer.data)

    def post(self, request):
        data = request.data
        ip = data['ip']

        self.snmp(ip)

        return Response()

    def snmp(self, ip):
        user = self.Meta.env('SNMP_USER')
        passw = self.Meta.env('SNMP_PASS')

        command = "snmpwalk -v3 -l authPriv -u %s -a MD5 -A %s -X %s %s .1.3.6.1.2.1.2.2.1.10" %(user, passw, passw, ip)

        print(command)
        return 0

    class Meta:
        app_label = 'gestor'
        env = environ.Env()
        environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/hmgru/.env')