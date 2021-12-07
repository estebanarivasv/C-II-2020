#!/usr/bin/python
import os, time

"""

--- Exercise statement: N°4 - fork

Escribir un programa que en ejecución genere dos procesos, uno padre y otro hijo.

El hijo debe escribir "Soy el hijo, PID YYYY" 5 veces (YYYY es el pid del hijo).

El padre debe escribir "Soy el padre, PID XXXX, mi hijo es YYYY" 2 veces (XXXX es el pid del padre).

El padre debe esperar a que termine el hijo y mostrar el mensaje "Mi proceso hijo, PID YYYY, terminó".

El hijo al terminar debe mostrar "PID YYYY terminando".

"""


def main():
    new_pid = os.fork()
    if new_pid == 0:
        for i in range(5):
            print("Soy el hijo. PID:", os.getpid())
            time.sleep(1)
        print("PID:", os.getpid(), "terminando.")
        os._exit(0)

    else:
        time.sleep(2)
        for i in range(2):
            print("Soy el padre. PID:", os.getpid(), ". Mi hijo es PID:", new_pid)
            time.sleep(1)

    (chld_pid, chld_status) = os.wait()
    if chld_status == 0:
        print("Mi proceso hijo PID:", chld_pid, "terminó.")


if __name__ == '__main__':
    main()
