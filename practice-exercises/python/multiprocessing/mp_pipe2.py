
from multiprocessing import Process, Pipe
import os,time

def f(r,w,nproc):
    print("nproc vale: %d" % nproc)
    if(nproc == 2):
        print("receptor")
        print("proc %d recibiendo: %s" % (os.getpid(),r.recv()))
        r.send("hello world")
    if(nproc == 1):
        print("emisor")
        w.send("proc %d enviando" % (os.getpid()))
        print(w.recv())
    r.close()
    w.close()

if __name__ == '__main__':
    r, w = Pipe()
    print("padre: %d" %os.getpid())
    p1 = Process(target=f, args=(r,w,1))
    p2 = Process(target=f, args=(r,w,2))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
