from hmgru.scriptsConsultas import consultaGeneral, generarReporte

import time
import environ
import logging

from hmgru.settings import BASE_DIR

logging.basicConfig(
    filemode='a',
    filename='Autocall.log',
    datefmt='%H:%M:%S',
    format='[%(asctime)s] %(msecs)d %(name)s: %(levelname)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

env = environ.Env()
environ.Env.read_env(BASE_DIR+"/hmgru/.env")

port = env('PORT')
timelaps = env.float('TIMELAPSE')

def consultaDatos():
    currentTime = time.strftime("%H:%M:%S")

    data = {
        'entrada': -1,
        'salida': -1,
        'edificios_entrada': [],
        'edificios_salida': []
    }

    logger.info("Consultando datos de red")  
    logger.info(currentTime)  

    while currentTime < "16:00:00":
        logger.info(data)
        data = consultaGeneral(port=port, previos=data)
        time.sleep(timelaps)
        currentTime = time.strftime("%H:%M:%S")

def reportar():
    logger.info("Reportando")
    generarReporte(port)
    logger.info("Reportado")
