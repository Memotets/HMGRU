from rest_framework.decorators import api_view
from rest_framework.response import Response

from database.models.DatosRed import DatosRed
from database.models.Reportes import Reporte
from database.models.Nodos import Nodos
from database.serializers.ReportesSerializer import ReportesSerializer
from database.serializers.NodosSerializaer import NodosSerializer

from bson import ObjectId
from urllib import request

import ast
import json

import environ
import datetime

import logging

logging.basicConfig(
    filemode='a',
    filename='Autocall.log',
    datefmt='%H:%M:%S',
    format='[%(asctime)s] %(msecs)d %(name)s: %(levelname)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@api_view(['GET'])
def cosultar_reporte(req):
    if req.method == 'GET':
        data = req.query_params
        fecha = data['fecha']
        tipo = data['tipo']
        ip = data['ip'] if 'ip' in data else None
        nodos = []

        datos_reporte = Reporte.objects.filter(tipo=tipo, diaReportado=fecha)

        if ip is not None:
            datos_reporte = datos_reporte.filter(edificio={'ip': ip})

        reporte = ReportesSerializer(datos_reporte[0]).data

        reporte['mediaTotal'] = ast.literal_eval(reporte['mediaTotal'])
        reporte['mediaEntrada'] = ast.literal_eval(reporte['mediaEntrada'])
        reporte['mediaSalida'] = ast.literal_eval(reporte['mediaSalida'])
        reporte['topNodos'] = ast.literal_eval(reporte['topNodos'])
        
        for top in reporte['topNodos']:
            try:
                id = top['nodo']
                datos_nodo = Nodos.objects.filter(_id=ObjectId(id)).first()
                print(datos_nodo)
                nodo = NodosSerializer(datos_nodo).data
                nodos.append(nodo)
            except:
                break

        return Response({'reporte': reporte, 'topNodos': nodos})

@api_view(['GET'])
def datos_reporte(request):
    

    env = environ.Env()
    environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')

    if(request.method == 'GET'):
        print("consultando")

        data = request.query_params
        fecha = data['fecha']
        port = env('PORT')

        f = datetime.date.today()
        print(f.strftime("%Y-%m-%d"))

        try:
            

            logger.info("Ligeros I")
            nodos_ligeros_i = reportar(fecha, 1, port, edificio=env.dict('LIGEROS_I'))
            logger.info("Ligeros II")
            nodos_ligeros_ii = reportar(fecha, 1, port, edificio=env.dict('LIGEROS_II'))
            nodos_pesados_i = reportar(fecha, 1, port, edificio=env.dict('PESADOS_I'))
            nodos_pesados_ii = reportar(fecha, 1, port, edificio=env.dict('PESADOS_II'))
            nodos_cafeteria = reportar(fecha, 1, port, edificio=env.dict('CAFETERIA'))
            nodos_govierno = reportar(fecha, 1, port, edificio=env.dict('GOBIERNO'))
            nodos_aulas_i = reportar(fecha, 1, port, edificio=env.dict('AULAS_I'))
            nodos_aulas_ii = reportar(fecha, 1, port, edificio=env.dict('AULAS_II'))

            tops = nodos_ligeros_i + nodos_ligeros_ii + nodos_pesados_i + nodos_pesados_ii + nodos_cafeteria + nodos_govierno + nodos_aulas_i + nodos_aulas_ii
            
            reportar(fecha, 0, port, tops=tops)
            
            return Response({'status': True})
        except Exception as e:
            logger.info(e)

def reportar(fecha, tipo, port, edificio=None, tops=None):
    logger.info("Reportando")
    consumos = consultaDatos(fecha, tipo, edificio['ip']) if edificio is not None else consultaDatos(fecha, tipo)
    logger.info(consumos)
    nodos = None
    mediaTotal = []
    mediaEntrada = []
    mediaSalida = []

    for consumo in consumos:
        mediaTotal.append({'valor': float(consumo[2])})
        mediaEntrada.append({'valor': float(consumo[1])})
        mediaSalida.append({'valor': float(consumo[0])})

    datos = { 
        'tipo': tipo,
        'mediaTotal': mediaTotal,
        'mediaEntrada': mediaEntrada,
        'mediaSalida': mediaSalida,
        'diaReportado': fecha
    }
    
    if tipo == 1:
        nodos = busquedaNodos(edificio['ip'], port, fecha)
        datos['edificio'] = edificio
    else:  
        print(len(tops))
        nodos = mergeSort(tops)
        
    if len(nodos) > 5:
        nodos = [nodos[0], nodos[1], nodos[2], nodos[3], nodos[4]]
        
    topNodos = []
    for nodo in nodos:
        topNodos.append(nodo)

    datos['topNodos'] = topNodos
    
    serializador_reporte = ReportesSerializer(data=datos)

    if serializador_reporte.is_valid():
        print("All  OK")
        serializador_reporte.save()
    else:
        print("Something went wrong")
        print(serializador_reporte.errors)
    
    return nodos
def consultaDatos(fecha, tipo, ip=None):
    inicio = [
        fecha+"T12:00:00.000Z", fecha+"T12:30:00.000Z", fecha+"T13:00:00.000Z", 
        fecha+"T13:30:00.000Z", fecha+"T14:00:00.000Z", fecha+"T14:30:00.000Z", 
        fecha+"T15:00:00.000Z", fecha+"T15:30:00.000Z", fecha+"T16:00:00.000Z", 
        fecha+"T16:30:00.000Z", fecha+"T17:00:00.000Z", fecha+"T17:30:00.000Z",
        fecha+"T18:00:00.000Z", fecha+"T18:30:00.000Z", fecha+"T19:00:00.000Z", 
        fecha+"T19:30:00.000Z", fecha+"T20:00:00.000Z", fecha+"T20:30:00.000Z",
    ]
    fin = [
        fecha+"T12:30:00.000Z", fecha+"T13:00:00.000Z", fecha+"T14:30:00.000Z",
        fecha+"T14:00:00.000Z", fecha+"T14:30:00.000Z", fecha+"T15:00:00.000Z",
        fecha+"T15:30:00.000Z", fecha+"T16:00:00.000Z", fecha+"T16:30:00.000Z",
        fecha+"T17:00:00.000Z", fecha+"T17:30:00.000Z", fecha+"T18:00:00.000Z",
        fecha+"T18:30:00.000Z", fecha+"T19:00:00.000Z", fecha+"T19:30:00.000Z",
        fecha+"T20:00:00.000Z", fecha+"T20:30:00.000Z", fecha+"T21:00:00.000Z",
    ]

    promedios = []

    try:
        for i in range(0,18):
            print(inicio[i])
            logger.info(inicio[i])
            datos = DatosRed.objects.filter(tipo = tipo, createdAt__gte = inicio[i], createdAt__lte = fin[i])
            logger.info(datos)
            
            if(tipo == 1):
                datos = datos.filter(edificio = {'ip': ip})

            count = 0
            prom_subida = 0
            prom_bajada = 0
            for dato in datos:
                count = count + 1
                prom_subida = prom_subida + dato.salida
                prom_bajada = prom_bajada + dato.entrada
            
            prom_subida = prom_subida / count if count != 0 else 0
            prom_bajada = prom_bajada / count if count != 0 else 0
            prom_consumo = prom_subida + prom_bajada

            promedios.append((prom_subida, prom_bajada, prom_consumo))
    except Exception as e:
        logger.info(e)

    return promedios

def busquedaNodos(ip, port, fecha):
    try:
        ''' Obtención de la lista de nodos de un edificio '''
        url = 'http://148.204.142.162:%s/database/lista/nodos/?ip=%s' %(port, ip)
        req = request.Request(url)
        res = request.urlopen(req).read()
        dec = res.decode('UTF-8') # Decodificación de la respuesta en UTF-8
        
        ''' Eliminación de errores de syntaxis JSON presentes  en la decodificación '''
        rep = dec.replace("\\", " ") # Eliminación de diagonales invertidas
        rep = rep.replace("\"{", "{") # Eliminación de comillas innecesarias 1
        rep = rep.replace("}\"", "}") # Eliminación de comillas innecesarias 2

        dict = json.loads(rep) # Conberción de la respuesta purgada en diccionario de Python

        nodos = dict['nodos'] # Separacion de los nodos del dicconario

        promedios = list() # Lista que almacenará los promedios de todos los nodos del edificio 

        inicio = fecha+"T00:00:00.000Z"
        fin = fecha+"T21:00:00.000Z" 

        print(inicio)
        print(fin)
        """ Obteción de los datos de tipo 2 del dia soliciado """
        nodos_monitoreados = DatosRed.objects.filter(tipo=2, createdAt__gte = inicio, createdAt__lte = fin) # filtro de los datos del nodo
        
        ''' Recorremos todos los nodos del edificio y calculamos sus promedios '''
        print('promedando nodos')
        for nodo in nodos:
            id = nodo['_id'] # _id del nodo que estamos consultando actualmente
            print(id)
            datos = nodos_monitoreados.filter(nodo = ObjectId(id)) # filtro de los datos por nodo
            
            promedio = 0 # Promedio de consumo del nodo
            promedio_entrada = 0
            promedio_salida = 0

            for dato in datos:
                promedio_entrada = promedio_entrada + dato.entrada
                promedio_salida = promedio_salida + dato.salida
                promedio = dato.entrada + dato.salida

            """
                Si existen registros del nodo calcula el promedio.
                Se hace esta comparación por si se da el caso de no existir registros
                    en los nodos de algun edificio dado a que no se consulto en el modulo
                    'lista nodos'
            """
            if len(datos) > 0:
                promedio_entrada = promedio_entrada / len(datos)
                promedio_salida = promedio_salida / len(datos)
                promedio = promedio / len(datos)

                elemento = {
                    'nodo': id, 
                    'mediaTotal': promedio, 
                    'mediaEntrada':promedio_entrada, 
                    'mediaSalida':promedio_salida
                }

                promedios.append(elemento)
                
        print('Nodos promediados')
        print('Ordenandos nodos')
        promedios = mergeSort(promedios)
        print('Nodos promediados')
        
        if len(promedios) > 5:
            return [promedios[0], promedios[1], promedios[2], promedios[3], promedios[4]]

        return promedios
    except Exception as ex:
        print(ex)
        return 'error'


def mergeSort(promedios):
    if len(promedios) <= 1:
        return promedios
    
    mid = len(promedios) // 2
    
    izq = promedios[:mid]
    der = promedios[mid:]

    ordenados = []

    izq_ordenada = mergeSort(izq)
    der_ordenada = mergeSort(der)

    i = 0
    j = 0

    while i < len(izq) and j < len(der):
        if izq_ordenada[i]['mediaTotal'] > der_ordenada[j]['mediaTotal']:
            ordenados.append(izq_ordenada[i])
            i += 1
        else:
            ordenados.append(der_ordenada[j])
            j += 1

    while i < len(izq):
        ordenados.append(izq_ordenada[i])
        i += 1

    while j < len(der):
        ordenados.append(der_ordenada[j])
        j += 1
        
    return ordenados