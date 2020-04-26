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


def send_signal(pid):
    os.kill(pid, signal.SIGUSR1)


def chld2_handler_USR1(signal, frame):
    print("I'm the child 2. PID =", os.getpid(), "\nPong!")


def handler_USR1(signal, frame):
    pass


def main():
    signal.signal(signal.SIGUSR1, handler_USR1)

    pid1 = os.fork()

    # Child no. 1
    if pid1 == 0:
        for i in range(10):
            ppid = os.getppid()
            print("\n\n-----------------------")
            send_signal(ppid)
            print("I'm the child 1. PID =", os.getpid(), "\nPing!")
            time.sleep(0.01)
        print("Finishing.")

    # Parent process
    elif pid1 != 0:

        pid2 = os.fork()

        # Child no. 2
        if pid2 == 0:
            signal.signal(signal.SIGUSR1, chld2_handler_USR1)
            while True:
                signal.pause()

        # Parent process
        elif pid2 != 0:
            while True:
                signal.pause()
                send_signal(pid2)


if __name__ == '__main__':
    main()
