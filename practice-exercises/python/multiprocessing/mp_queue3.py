import multiprocessing
import time, os


def escritor(numbers,q,pipe_w):
    print("Escritor escribiendo %d" % os.getpid())
    for i in numbers:
        q.put("insertando... %d" % i)
        time.sleep(1)
    pipe_w.send("hola")
    pipe_w.close()
    print("Terminando hijo %d..." % os.getpid())

def lector(q,pipe_r):
    print("Lector esperando...")
    valor = pipe_r.recv() # sincronismo ?
    pipe_r.close()
    while q:
        print("Lector leyendo: %s" % q.get())
        if q.empty():
            print("Cola vacia... saliendo")
            break



if __name__ == "__main__":
    r,w = multiprocessing.Pipe()
    q = multiprocessing.Queue()

    p1 = multiprocessing.Process(target=escritor, args=(range(5), q, w))
    p2 = multiprocessing.Process(target=lector, args=(q, r))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("Padre terminando...")
