from multiprocessing import Process, Queue
import os

def f(q):
    q.put([42, None, 'hello', os.getppid(), os.getpid()])

if __name__ == '__main__':
    q = Queue()
    q.put("hola mundo")
    print("El contenido de la cola es: %s" % q.get())

    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
