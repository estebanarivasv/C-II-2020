#!/usr/bin/python
import time
import os
import signal

"""

--- Exercise statement: N°6 - ping_pong

Realice un programa que genere dos procesos.

El proceso hijo1 enviará la señal SIGUSR1 al proceso padre y mostrará la cadena "Soy el hijo1 con PID=XXXX: ping" cada 5 segundos.

El proceso padre, al recibir la señal SIGUSR1 enviará esta misma señal al proceso hijo2. El proceso hijo2, al recibir dicha señal mostrará la cadena "Soy el hijo2 con PID=YYYY: pong" por pantalla.

Este comportamiento se deberá detener a las 10 señales enviadas por el proceso hijo1.

Soy proceso hijo1 con PID=1545: "ping"
Soy proceso hijo2 con PID=1547: "pong"

[... 5 segundos mas tarde ...]
Soy proceso hijo1 con PID=1545: "ping"
Soy proceso hijo2 con PID=1547: "pong"
[... y así sucesivamente ...]


"""


def handler_hijo(s, f):
    print("My parent PID %d sent me a SIGUSR1 signal." % os.getppid())


def handler_padre(s, f):
    print("Goodbye! Finishing execution.")
    signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    pid = os.fork()

    if pid == 0:
        signal.signal(signal.SIGUSR1, handler_hijo)
        while True:
            signal.pause()
    else:
        signal.signal(signal.SIGINT, handler_padre)
        for i in range(10):
            time.sleep(10)
            os.kill(pid, signal.SIGUSR1)
        print("Parent killing son.")
        os.kill(pid, signal.SIGTERM)


if __name__ == '__main__':
    main()
