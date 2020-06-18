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


import subprocess as sp
import socket
import sys
import getopt
import multiprocessing


if __name__ == '__main__':

