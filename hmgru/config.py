from hmgru.scheduler import initThread

#preload_app = True

def when_ready(server):
    server.log.info("Server is ready. Spawning workers")
    initThread()


    
    
