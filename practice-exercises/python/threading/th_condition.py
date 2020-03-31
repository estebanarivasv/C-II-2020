import random, time
from threading import Condition, Thread
"""
la variable de condicion será usada para reprsentar la disponibilidad de un item producido
"""
condition = Condition()

box = []

def producer(box, nitems):
    for i in range(nitems):
        time.sleep(random.randrange(2, 5))  
        condition.acquire()
        print("Productor adquiriendo...")
        num = random.randint(1, 10)
        box.append(num)  
        condition.notify()  
        print("Producido: ", num)
        condition.release()
def consumer(box, nitems):
    for i in range(nitems):
        condition.acquire()
        print("Consumidor adquiriendo...")
        condition.wait()  # Blocks until an item is available for consumption.
        print("%s: Acquired: %s" % (time.ctime(), box.pop()))
        condition.release()
threads = []
"""
nloops es el número de veces que el item será producido y consumido
"""
nloops = random.randrange(3, 6)
for func in [producer, consumer]:
    threads.append(Thread(target=func, args=(box, nloops)))
    threads[-1].start()  
for thread in threads:
    thread.join()
print("All done.")
