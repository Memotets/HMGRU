import time
import threading
import environ

from scriptsConsultas import *

class AutocallController:

    def __init__(self) :
        self.env = environ.Env()
        environ.Env.read_env('/home/upiiz/Documents/sistemas/hmgru/hmgru/.env')

    def autocall(self, startTime, endTime, octetos):
        currentTime = time.strftime("%H:%M:%S")
        while (currentTime != endTime):#avoid recusive problems
            currentTime = time.strftime("%H:%M:%S")
            #Call request
            octetos = consultaGeneral(previos = octetos)
            time.sleep(self.env.float('TIMELAPSE')) #espera de 10 ms
        self.timer(startTime, endTime, octetos)

    def timer(self, startTime, endTime, octetos):
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

        self.autocall(startTime, endTime, octetos)

    def initThread(self):
        timerThreat = threading.Thread(target=self.timer,args=("07:00:00", "16:00:00", {'entrada': 0, 'salida': 0}))
        timerThreat.start()