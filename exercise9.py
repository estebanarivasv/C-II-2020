import sys
import getopt
import os
import signal
import time

"""

--- Exercise statement: N°9 - 

Escribir un programa que genere un proceso hijo (fork), y a su vez, éste genere un nuevo proceso hijo (fork) (ver 
esquema abajo). Todos los procesos estarán comunicados mediante un pipe.

     A → B →C

El proceso B escribirá en el pipe el mensaje "Mensaje 1 (PID=BBBB)\n" en el momento en que el proceso A le envíe la 
señal USR1.

Cuando esto ocurra, el proceso B le enviará la señal USR1 al proceso C, y C escribirá en el pipe el mensaje "Mensaje 2 
(PID=CCCC)\n".

Cuando el proceso C escriba este mensaje, le enviará al proceso A la señal USR2, y el proceso A leerá el contenido del
pipe y lo mostrará por pantalla, en el formato:

A (PID=AAAA) leyendo:
Mensaje 1 (PID=BBBB)
Mensaje 2 (PID=CCCC)

Notas:

    AAAA, BBBB, y CCCC son los respectivos PIDs de los procesos A, B y C.
    Inicialmente el proceso B envía un mensaje al pipe cuando A le hace llegar la señal USR1, por lo que B deberá 
quedar esperando al principio una señal.
    El proceso C también deberá quedar esperando inicialmente una señal que recibirá desde el proceso B para 
poder realizar su tarea.
    El proceso A inicialmente envía la señal USR1 al proceso B, y automáticamente debe quedar esperando una señal 
desde el proceso C para proceder a leer desde el pipe.
    Los saltos de línea en los mensajes (“\n”) son necesarios para que el pipe acumule varias líneas, y no concatene
los mensajes en la misma línea.
    El pipe es uno solo en el que los procesos B y C deberán escribir, y el proceso A deberá leer.
    Pista: la utilización de señales es para sincronizar los procesos, no necesariamente los handlers deben 
gestionar el pipe.


"""


def main():
    pass


if __name__ == '__main__':
    main()
