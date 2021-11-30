from sre_constants import error
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from authentication.usuarioForm import UsuariosEditForm, UsuariosForm

import environ
import re
import random
import string

#seguimiento particular de un nodo
from database.models.Nodos import *
from bson import ObjectId

# Create your views here.
from django.views.generic import TemplateView

env = environ.Env()
environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')
port = env("PORT")
edificios = [
    env.dict('LIGEROS_I'),
    env.dict('LIGEROS_II'),
    env.dict('PESADOS_I'),
    env.dict('PESADOS_II'),
    env.dict('CAFETERIA'),
    env.dict('GOBIERNO'),
    env.dict('AULAS_I'),
    env.dict('AULAS_II')
]


def index(request):
    return redirect('grafica.general')

#def logInView(request):
    #return render(request, "pages/logIn.html", {"port" :port})

@login_required
def GeneralGraphView(request):
    return render(request, "pages/graficaGeneral.html", {"port" :port})

@login_required
def BuildingListView(request):
    return render(request, "pages/listaEdificios.html", {"edificios": edificios, "port": port})

@login_required
def BuildingGraphView(request):
    return render(request, "pages/graficaEdificio.html", {"edificios": edificios, "port": port})
    
@login_required
def NodeGraphView(request, id):
    context = {}
    context["port"]         = port
    context["node"]         = Nodos.objects.get(_id = ObjectId(id))
    context["id"]           = id
    context["edificios"]    = edificios
    return render(request, "pages/graficaNodo.html", context)

@login_required
def ReportGenerator(request):
    return render(request, "pages/generarReporte.html", {"edificios": edificios, "port": port})

def Salir(request):
    print('loging out')
    logout(request)
    return redirect('/')

@login_required
def RegistroView(request):
    if request.method == 'GET':
        return render(request, "pages/signup.html")
    if request.method == 'POST':
        datos_usuario = request.POST.dict()
        password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

        datos_usuario['password1'] = password
        datos_usuario['password2'] = password

        print('password1: %s' %datos_usuario['password1'])
        print('password2: %s' %datos_usuario['password2'])

        data = {
            'form': datos_usuario
        }

        if len(datos_usuario['rfc']) < 13:
            data['status'] = 'error'
            messages = {
                'rfc': 'El RFC debe contener 13 caracteres'
            }
            data['messages'] = messages
        else:
            form = UsuariosForm(datos_usuario)
            if form.is_valid():
                usuario = form.save()
                print('usuario creado')
                data['status'] = 'success'
                data['messages'] = password
            else:
                data['status'] = 'error'
                data['messages'] = form.error_messages

                if data['messages']['password_mismatch']:
                    data['messages']['password_mismatch'] = '''
                    El RFC ya está registrado
                    ''' 

        return render(request, 'pages/signup.html', data)

@login_required
def PerfilView(request):
    if request.method == "POST":
        data = request.POST
        
        usuario = request.user
        if data['operacion'] == 'change_password':
            if usuario.check_password(data['password']):
                pass1 = data['newPassword1']
                pass2 = data['newPassword2']

                if(pass1 == pass2):
                    errors = False
                    messages = list()
                    exp = re.match('^(?=\w*\d)(?=\w*[A-Z])(?=\w*[a-z])', pass1)

                    if len(pass1) < 8:
                        errors = True
                        messages.append('La contraseña debe contener al menos 8 caracteres')
                    if not exp:
                        errors = True
                        messages.append("La contraseña debe contener al menos un numero, una mayúscula y una munúscula")
                    
                    if errors:
                        return render(request, 'pages/perfil.html', {'error_messages': messages})    

                    usuario.set_password(pass1)
                    usuario.save()
                    return render(request, 'pages/perfil.html', {'password_success': True})
                else:
                    return render(request, 'pages/perfil.html', {'error_messages': ["Los campos no coinciden"]})
            else:
                return render(request, 'pages/perfil.html', {'error_messages': ["Las contraseña es incorrecta"]})
        else:
            form = UsuariosEditForm(data, instance=usuario)

            if(form.is_valid()):
                request.user = form.save()
                print("Actualizado correctamente")
            else:
                print("Error al actualizar")
                print(form.errors)
                
        
    return render(request, 'pages/perfil.html')
    

def page404View(request, *args, **kwargs):
    print("hola")
    return render(request, 'pages/404.html')