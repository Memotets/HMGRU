#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import time
import threading
import environ

#from scriptsConsultas import *


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmgru.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.runserver import Command as settings

        settings.default_addr = "148.204.142.162"
        settings.default_port = "3031"
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def autocall(startTime, endTime, octetos):
    currentTime = time.strftime("%H:%M:%S")
    while (currentTime != endTime):#avoid recusive problems
        currentTime = time.strftime("%H:%M:%S")
        #Call request
        #print("Autocall running on Current time: "+currentTime)
        #octetos = consultaGeneral(previos = octetos)
        time.sleep(float(env('TIMELAPSE'))) #espera de 20 ms
    timer(startTime, endTime, octetos)

def timer(startTime, endTime, octetos):
    currentTime = time.strftime("%H:%M:%S")

    print(currentTime)
    while (currentTime != startTime):#avoid recusive problems
        currentTime = time.strftime("%H:%M:%S")
        #in case something went wrong
        if((startTime<endTime and startTime<currentTime and endTime>currentTime) or 
        (startTime>endTime and startTime>currentTime and endTime<currentTime)):
            #something when wrong so we reactive te serv or serv was active lately
            #print("Autocall will running on Current time: "+currentTime)
            break

        #waiting time
        #print("Autocall not calling: "+currentTime)
        #octetos = consultaGeneral(octetos)

        if (startTime ==  "07:00:00" and endTime == "16:00:00"):
            currentSec = time.strftime("%S")
            currentMin = time.strftime("%M")
            if (currentSec == "00" and currentMin == "00"):
                #one hr wait
                time.sleep(3600)
            elif (currentSec == "00" and currentMin != "00"):
                #one min wait
                time.sleep(60)
            else:
                #one sec wait
                time.sleep(1)
        else:
            #Test cases
            time.sleep(1)

    autocall(startTime, endTime, octetos)

timerThreat = threading.Thread(target=timer,args=("07:00:00", "16:00:00", {'entrada': 0, 'salida': 0}))
env = environ.Env()

if __name__ == '__main__':
    environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')
    timerThreat.start()
    main()
