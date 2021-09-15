from rest_framework.decorators import api_view
from rest_framework.response  import Response

from bson import ObjectId

from database.models.Nodos import Nodos
from database.serializers.NodosSerializaer import NodosSerializer

from paramiko.ssh_exception import AuthenticationException, BadHostKeyException, SSHException

import paramiko
import time
import environ
import ast

""" Cambia el estado administrativo de uno o varios nodos dentro de la red """
@api_view(['PUT'])
def toggle_view(request):
    env = environ.Env()
    environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')

    if(request.method == 'PUT'):
        code = 200
        message = "success"

        print("entrando al put")
        data = request.data

        ip = data['ip']
        nodos = data['nodos']

        print(isinstance(nodos, list))

        ssh_username = env('SSH_USERNAME')
        ssh_key = env('SSH_ALTERNATIVE_KEY') if ip == '10.204.142.246' else env('SSH_KEY')

        try:
            algorithms = {
                'kex': 'diffine-hellman-group1-sha-1'
            }

            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect(hostname=ip, username=ssh_username, password= ssh_key, disabled_algorithms=algorithms, banner_timeout=30)

            channel = ssh_client.invoke_shell()

            for nodo in nodos:
                new_state = 'disable' if nodo['activoAdministrativo'] else 'enable'

                command = 'set port %s %s\n' %(new_state, nodo['idPuerto'])
                channel.send(command)
                
                time.sleep(5)
                
                UpdateNodo(nodo['_id'], nodo['activoAdministrativo'])

        except AuthenticationException:
            print("Authentication has failed")

            code = 400
            message = "La autenticacion SSH ha fallado"
        except SSHException as ssh_exception:
            print("Unable to establish SSH connection: %s" % ssh_exception)

            code = 400
            message = "No se pudo establecer la coneccion SSH: %s" %ssh_exception
        except BadHostKeyException as badHostKeyException:
            print("Unable to verify server's host key: %s" % badHostKeyException)

            code = 400
            message = "No se pudo verificar las claves con el servidor: %s" %badHostKeyException
        except Exception as e:
            print("Unknoun esception: %s" % e)

            code = 400
            message = "Error desconocido: %s" %e
        
        ssh_client.close()

        response = {
            "code": code,
            "message": message
        }

        return Response(response)
    else:
        print(request.method)

def UpdateNodo(id, estado):

    nodo = Nodos.objects.filter(_id=ObjectId(id)).first()
    
    nuevo_estado = not estado
    
    serializer = NodosSerializer(nodo, data={'activoAdministrativo': nuevo_estado}, partial=True)
    
    if serializer.is_valid():
        serializer.save()
    else: 
        print("not valid")

@api_view(['GET'])
def Prueba(request):
    #nodo = Nodos.objects.all()
    texto = '60da2b2cf5b0eaaec3e6a5ee'
    nodo = Nodos.objects.filter(_id=ObjectId(texto)).first()
    serializer = NodosSerializer(nodo)
    return Response(serializer.data)
    

