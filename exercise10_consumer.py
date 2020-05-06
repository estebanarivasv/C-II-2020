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
    pipe_output = '/tmp/greeting'

    lines = ""

    # Consumer gets the greeting
    fifo = open(pipe_output, 'r')
    lines = fifo.readlines()
    fifo.close()

    r, w = os.pipe()
    child = os.fork()

    if not child:
        # Child sentences, reads greeting from pipe
        os.close(w)
        read_head = open(r, 'r')
        greeting = read_head.readlines()
        print("Producer sends greetings: ")
        for line in greeting:
            print(line)
    else:
        # Parent sentences, writes greeting in pipe
        os.close(r)
        write_head = open(w, 'w')
        write_head.writelines(lines)
        write_head.flush()
        write_head.close()


if __name__ == '__main__':
    main()
