from time import time
from hmgru.AutocallController import consultaDatos, reportar

import schedule
import threading
import time

schedule.every().monday.at("07:00:00").do(consultaDatos)
schedule.every().tuesday.at("07:00:00").do(consultaDatos)
schedule.every().wednesday.at("11:50:00").do(consultaDatos)
schedule.every().thursday.at("07:00:00").do(consultaDatos)
schedule.every().friday.at("07:00:00").do(consultaDatos)

schedule.every().monday.at("18:00:00").do(reportar)
schedule.every().tuesday.at("18:00:00").do(reportar)
schedule.every().wednesday.at("18:00:00").do(reportar)
schedule.every().thursday.at("18:00:00").do(reportar)
schedule.every().friday.at("18:00:00").do(reportar)

def reloj():
    while True:
        schedule.run_pending()
        time.sleep(1)

def initThread():
    timer = threading.Thread(target=reloj)
    timer.start()