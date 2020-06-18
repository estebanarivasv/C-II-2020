"""

--- Exercise statement: N°16 - queue

Escriba un programa que cree diez procesos hijos (multiprocessing).

Cada proceso al iniciar debe escribir por pantalla "Proceso n, PID: xxxx"

A su vez, cada proceso debe esperar n segundos, donde n es el número de proceso hijo, y luego escribir en un formato
"xxxx\t" el pid en una cola de mensajes.

El padre debe esperar a que todos los hijos terminen, y luego leer el contenido de la cola de mensajes y mostrarlo por
pantalla.

Tag: mp_mq
"""

import subprocess as sp
import socket
import sys
import getopt
import multiprocessing
import os
import time


def child_prints(proc_num, q):
    print(f"\nProcess no. {proc_num}, PID: {os.getpid()}")
    time.sleep(proc_num)
    q.put(f"{os.getpid()}\t")


if __name__ == '__main__':
    q = multiprocessing.Queue()
    child = []
    for i in range(10):
        j = i + 1
        child_proc = multiprocessing.Process(target=child_prints, args=(j, q,))
        child.append(child_proc)
        child[i].start()
        child[i].join()

    while True:
        try:
            while True:
                data = q.get(True, 2)
                print(f"Receiving from children: {data}")
        except Exception:
            print(f"Empty queue.")
        break
    print("Parent exiting.")
