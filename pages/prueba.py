from rest_framework.views import APIViews
from rest_framework.response import Response
# Create your views here.
@api_view(['GET'])

def Prueba(request):
    env = environ.Env()
    environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')
    texto={"texto":"Hola mundo"}
    return Response(texto)