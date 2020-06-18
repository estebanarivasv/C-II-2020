"""

--- Exercise statement: N°15 - pipes

Escribir un programa que lance dos procesos hijos (multiprocessing).

Uno de los procesos hijos se encargará de leer desde la entrada estándar líneas de texto, y en la medida en que el
usuario escriba, el proceso las irá enviando por un pipe que compartirá con el otro proceso hijo (multiprocessing.Pipe)

El segundo proceso se encargará de leer desde el pipe las líneas que el primer proceso escriba, y las irá mostrando por
pantalla en el formato “Leyendo (pid: 1234): mensaje”, donde 1234 es el pid de este segundo proceso, y “mensaje” es el
contenido leído desde el pipe.

Tag: mp_pipe
"""

import sys
import multiprocessing
import os
import time
import signal


def signal_handler(signal, frame):
    print("Exiting...")
    sys.exit(0)


def from_STDIN_reader(a):
    # leer lineas desde stdin y enviar por pipe a p2
    signal.signal(signal.SIGINT, signal_handler)
    sys.stdin = open(0)  # Gets stdin working in the process 1
    while True:
        data = input("> ")
        if data == "":
            break
        a.send(data)
        print(f"\n\n_______________________\nSending data to second process\n_______________________")
        time.sleep(4)
    print("Proc1 done!")


def from_PIPE_reader(b):
    # leer desde pipe y mostrar por pantalla
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        data = b.recv()
        time.sleep(2)
        print(f"_______________________\nReading pid:{os.getpid()}, message: {data}\n_______________________")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    a, b = multiprocessing.Pipe()
    proc1 = multiprocessing.Process(target=from_STDIN_reader, args=(a,))
    proc2 = multiprocessing.Process(target=from_PIPE_reader, args=(b,))
    proc1.start()
    proc2.start()
