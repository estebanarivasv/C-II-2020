#!/usr/bin/python
import getopt
import sys
import os

"""

--- Exercise statement: N°6 - fork

Realice un programa que genere N procesos hijos. Cada proceso al iniciar deberá mostrar:

“Soy el proceso N, mi padre es M” N será el PID de cada hijo, y M el PID del padre.

             padre

          /   |   \

    hijo1   hijo2   hijo3

La cantidad de procesos hijos N será pasada mediante el argumento "-n" de línea de comandos.

"""


def child_speaking():
    print("Soy el proceso ", os.getpid(), "y mi padre es", os.getppid())
    os._exit(0)


def main():
    chld_num = 0

    (opts, args) = getopt.getopt(sys.argv[1:], "n:")
    for (opt, arg) in opts:
        if opt == "-n":
            chld_num = int(arg)
            print(chld_num)

    for i in range(chld_num):
        new_chld = os.fork()
        if new_chld == 0:
            child_speaking()


if __name__ == '__main__':
    main()
