"""

--- Exercise statement: N°19 - Lock/RLock (multiprocessing)

Escriba un programa que lance N procesos hijos. El programa recibirá la cantidad de procesos por argumento con -n.

El programa recibirá, mediante el uso del modificador “-f”, un nombre de archivo que deberá crear o, si ya existe,
abrir y limpiar.

Además, recibirá por argumento un número mediante el modificador “-r”. Ese número representará la cantidad de
iteraciones (ver más adelante).

Una llamada típica al programa podría ser:

./programa -n 15 -r 5 -f /tmp/test.txt

Cada proceso tendrá asociada una letra del alfabeto (A, B, C, etc.), y deberá escribir “su” letra tantas
veces como iteraciones se hayan especificado con “-r”, y con un delay de 1 segundo.

Es decir, con la llamada anterior, cada proceso deberá escribir una letra (“A”, “B”, etc) 5 veces con
intervalo de un segundo.

Haga uso de lock para que las R letras (5 en el ejemplo) escritas por cada proceso se mantengan juntas
y no intercaladas con los demás.

El resultado en el archivo del ejemplo será algo así:

AAAAADDDDDEEEEEBBBBB …
Y no algo así

AABADDEBABEFBFAGGHD…

"""

import getopt
import sys
import string
import random
import multiprocessing
import time
import os


def runProcess(r, l, file_route):
    letter = random.choice(string.ascii_letters)
    l.acquire()
    file = open(file_route, mode='a')
    for i in range(int(r)):
        time.sleep(1)
        file.write(letter)
        print(f"Proc {os.getpid()} wrote in file letter {letter}")
    l.release()
    file.close()


if __name__ == '__main__':
    lock = multiprocessing.Lock()
    if len(sys.argv[1:]) > 1:

        proc_num = 0
        file_route = ""
        iterations = 0

        (option, value) = getopt.getopt(sys.argv[1:], "n:f:r:")
        print(option)
        for (opt, val) in option:
            if opt == "-n":
                proc_num = int(val)
            if opt == "-f":
                file_route = val
            if opt == "-r":
                iterations = int(val)

        for i in range(proc_num):
            p = multiprocessing.Process(target=runProcess, args=(iterations, lock, file_route))
            p.start()
            p.join()

    else:
        print("Usage example: python3 exercise19_multiprocessing_lock.py -n 15 -r 5 -f /tmp/test.txt")
