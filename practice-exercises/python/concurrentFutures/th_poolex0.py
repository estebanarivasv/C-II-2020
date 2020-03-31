from concurrent.futures import ThreadPoolExecutor
from time import sleep

def return_after_5_secs(message):
    sleep(5)
    return message

#establecemos el número de hilos, por default son 5
pool = ThreadPoolExecutor(3)

# enviamos una tarea al pool
future = pool.submit(return_after_5_secs, ("hello"))

#future.done será verdadero si el pool termino de ejecutar la tarea, sino falso
print(future.done())
sleep(5)
print(future.done())
print(future.result())
