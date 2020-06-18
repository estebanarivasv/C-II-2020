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


if __name__ == '__main__':

