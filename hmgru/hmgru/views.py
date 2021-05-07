from django.http import HttpResponse

from urllib import request as url_request
from urllib import parse

import ast
from scriptsConsultas import *

def pruebas(request):

    data = consultaGeneral()

    print(data)

    return HttpResponse(data)