#!/usr/bin/python
import time
import os
import signal

"""

--- Exercise statement: N°6 - SIGUSR1 SIGINT

Desde un proceso padre crear un hijo y enviarle una señal SIGUSR1 cada 5 segundos.

El proceso hijo estará a la espera y escribirá un aviso en pantalla cada vez que llega la señal de su padre.

Este comportamiento se detendrá luego de haber enviado 10 señales, o cuando el proceso padre reciba la señal de 
interrupción SIGINT, deberá mostrar un mensaje de despedida en pantalla, y terminar la ejecución.


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
