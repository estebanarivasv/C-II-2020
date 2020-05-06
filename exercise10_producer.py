import sys
import getopt
import os
import signal
import time

"""

--- Exercise statement: N°10 - consumer

Crear un sistema Productor-Consumidor (Escritor-Lector) donde un proceso productor almacene un mensaje de saludo en una 
tubería FIFO. Ese mensaje será enviado mediante línea de comandos como argumento del programa. Ejemplo

./saludofifo "HOLA MUNDO"

Otro programa (consumidor) deberá leer el mensaje desde la tubería FIFO, generar un proceso hijo (fork) y enviarle por 
PIPE el mensaje al hijo.

El proceso hijo mostrará por pantalla el mensaje recibido.

Proc1_fifo_escritor → FIFO → Proc2_fifo_lector → pipe → Proc2hijo


"""


def main():
    pipe_input = '/tmp/greeting'

    greeting = sys.argv[1:]

    fifo = open(pipe_input, "w")
    for line in greeting:
        fifo.write(line)
    fifo.flush()
    fifo.close()
    print("Producer says: ")
    for line in sys.argv[1:]:
        print(line)


if __name__ == '__main__':
    main()
