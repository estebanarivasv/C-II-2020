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


def pA_USR2_handler(signal, frame):
    print("A (PID=%d) leyendo:\n" % os.getpid())


def pB_USR1_handler(signal, frame):
    print("Message 1 (PID=%d)\n" % os.getpid())


def pC_USR1_handler(signal, frame):
    print("Message 2 (PID=%d)\n" % os.getpid())


def main():
    pipe_path = '/tmp/shared_pipe'

    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)

    parent = os.fork()

    # Parent's sentences (PROCESS A)
    if parent:
        signal.signal(signal.SIGUSR2, pA_USR2_handler)
        child_pid = parent
        time.sleep(2)
        os.kill(child_pid, signal.SIGUSR1)
        print("señal enviada y pc A entrando en espera")
        signal.pause()
        pipe_output = open(pipe_path, 'r')

        for line in pipe_output:
            print(line)

        os.wait()
        os._exit(0)

    else:
        grandparent_pid = os.getppid()
        child = os.fork()

        # Child's sentences (PROCESS B)
        if child:
            signal.signal(signal.SIGUSR1, pB_USR1_handler)
            signal.pause()
            print("señal recibida y pc B escribiendo en pipe")
            grandchild_pid = child
            pipe_in = open(pipe_path, 'w')
            pipe_in.write("Message 1 (PID=%d)\n" % os.getpid())
            pipe_in.close()
            os.kill(grandchild_pid, signal.SIGUSR1)
            print("señal enviada")
            time.sleep(4)
            os._exit(0)

        # Grandchild's sentences (PROCESS C)
        else:
            signal.signal(signal.SIGUSR1, pC_USR1_handler)
            signal.pause()
            print("señal recibida y pc C escribiendo en pipe")
            pipe_in = open(pipe_path, 'w')
            
            pipe_in.write("Message 2 (PID=%d)\n" % os.getpid())
            pipe_in.close()
            time.sleep(1)
            os.kill(grandparent_pid, signal.SIGUSR2)
            print("señal enviada")
            os._exit(0)


if __name__ == '__main__':
    main()
