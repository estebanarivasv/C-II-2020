#!/usr/bin/python
import time
import os
import signal

"""

--- Exercise statement: N°7 - ping_pong

Realice un programa que genere dos procesos.

El proceso hijo1 enviará la señal SIGUSR1 al proceso padre y mostrará la cadena "Soy el hijo1 con PID=XXXX: ping" 
cada 5 segundos. 

El proceso padre, al recibir la señal SIGUSR1 enviará esta misma señal al proceso hijo2. El proceso hijo2, 
al recibir dicha señal mostrará la cadena "Soy el hijo2 con PID=YYYY: pong" por pantalla. 

Este comportamiento se deberá detener a las 10 señales enviadas por el proceso hijo1.

Soy proceso hijo1 con PID=1545: "ping"
Soy proceso hijo2 con PID=1547: "pong"

[... 5 segundos mas tarde ...]
Soy proceso hijo1 con PID=1545: "ping"
Soy proceso hijo2 con PID=1547: "pong"
[... y así sucesivamente ...]


"""


def USR1_chld_handler(signal, frame):
    print("I'm the child No. 2\tPID: ", os.getpid(), ": pong")


def USR1_parent_handler(signal, frame):
    pass


def main():
    child1 = os.fork()
    child2 = os.fork()

    # CHILD PROCESS No. 1
    if child1 == 0:
        for i in range(10):
            print("I'm the child No. 1\tPID: ", os.getpid(), ": ping")
            os.kill(int(os.getppid()), signal.SIGUSR1)
            time.sleep(5)

    # CHILD PROCESS No. 2
    if child2 == 0:
        signal.signal(signal.SIGUSR1, USR1_chld_handler)
        while True:
            signal.pause()

    # PARENT PROCESS
    else:
        signal.signal(signal.SIGUSR1, USR1_parent_handler)
        while True:
            signal.pause()
            os.kill(child2, signal.SIGUSR1)


if __name__ == '__main__':
    main()
