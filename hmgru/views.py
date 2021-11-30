from django.http import HttpResponse
from django.shortcuts import redirect

from authentication.usuarioForm import UsuariosForm

import random
import string

def pruebas(request):
    print(request.method)
    if request.method == 'POST':
        print('in post function')
        datos_usuario = request.POST.dict()
        password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

        datos_usuario['password1'] = password
        datos_usuario['password2'] = password

        print(datos_usuario)
        messages = ''

        form = UsuariosForm(datos_usuario)
        if form.is_valid():
            usuario = form.save()
            print('usuario creado')
            messages = 'El usuario se creo con la contraseña: %s' %password
            print(messages)
            return HttpResponse(messages)

        print(form.errors)
        return HttpResponse(form.errors.as_data())

def pruebas(request, status, message):
    print(status)
    print(type(message))
    return HttpResponse()