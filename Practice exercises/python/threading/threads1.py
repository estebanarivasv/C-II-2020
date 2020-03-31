import sys
import threading
import time

DELAY=5

def thread_function(name):
    print("Iniciando hilo %s" % name)
    time.sleep(DELAY)
    print("Finalizando hilo %s, se acabó el tiempo" % name)


if __name__ == "__main__":

    print("Iniciando programa principal, antes de crear el thread")

    x = threading.Thread(target=thread_function, args=(1,))
    
    print("Programa principal, thread creado, antes de lanzarlo...")

    x.start()

    print("Programa principal: thread lanzado!")

    print("Programa principal, terminando ¿?")

    print("\n ==> Tiene %d segundos para abrir otra terminal y ejecutar \" ps -eLf | grep %s | grep -v grep \" " % (DELAY, sys.argv[0]))
