import os,time,signal

def handler(s,f):
    print("mensaje...")

def hijo():
    print("Iniciando hijo")
    while True:
        print("Hijo esperando...")
        signal.pause()


signal.signal(signal.SIGUSR1,handler)
pid=os.fork()
print("pid: %d\n" % pid)

if pid == 0:
    hijo()
else:
    print("Iniciando padre")
    for item in range(5):
        os.kill(pid,signal.SIGUSR1)
        time.sleep(1)
    print("Padre matando al hijo...")
    os.kill(pid,signal.SIGTERM)
    print("Padre terminando...")



        
