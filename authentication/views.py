from django.http.response import HttpResponseRedirect
from authentication.usuarioForm import UsuariosForm
from django.urls import reverse

from hmgru.views import pruebas

import random
import string

# Create your views here.
def register(request):
    if request.method == 'POST':
        datos_usuario = request.POST.dict()
        password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))

        datos_usuario['password1'] = password
        datos_usuario['password2'] = password

        print('password1: %s' %datos_usuario['password1'])
        print('password2: %s' %datos_usuario['password2'])

        status = ''
        messages = []

        #if len(datos_usuario['status']) < 13:
        #    status = False
        #    messages = messages.append('El RFC debe contener 13 caracteres')

        form = UsuariosForm(datos_usuario)
        if form.is_valid():
            usuario = form.save()
            print('usuario creado')
            status = 'success'
            messages = 'El usuario se creo con la contraseña: <b>%s</b>' %password
        else:
            status = 'error'
            messages = form.error_messages
        
        return HttpResponseRedirect(reverse('registro.view.return', kwargs=({'status':status, 'message':messages})))
        #return HttpResponse(form.errors.as_data())
            