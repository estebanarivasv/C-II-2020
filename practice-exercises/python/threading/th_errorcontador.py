import threading, time

NTHREADS=5
NITER=1000000

contador=0

def count():
    global contador
    for i in range(NITER):
        tmp = contador
        tmp = tmp+1
        contador = tmp



hilos = []
for i in range(5):
    hilos.append(threading.Thread(target=count, ))
    hilos[-1].start()


for i in range(5):
    hilos[i].join()

if (contador != NTHREADS*NITER):
    print("NOOOOOO! contador es [%d] y deberia ser %d" % (contador, NITER*NTHREADS))
else:
    print("Bien!! contador vale %d" % contador)


