from rest_framework.views import APIView
from rest_framework.response import Response

from database.models.ErroresSistema import ErroresSistema

class ErroresSistemaView(APIView):

    def get(self, request):
        errores = ErroresSistema.objects.all()
        return Response()

    class Meta:
        aoo_label = 'gestor'