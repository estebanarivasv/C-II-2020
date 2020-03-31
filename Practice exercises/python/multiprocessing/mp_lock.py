
from multiprocessing import Process, Lock
import time

def f(l, n):
    l.acquire()
    for i in range(3):
        print ("hello world %d %d" % (n,i))
        time.sleep(1)
    l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(2):
        Process(target=f, args=(lock, num)).start()
