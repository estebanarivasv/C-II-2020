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


def write_to_fifo(write_head, message):
    w = write_head
    with open(w, 'w') as w:
        w.write(message)
    w.close()


def read_from_fifo(read_head):
    r = read_head
    with open(r, 'r') as r:
        print("Process A (PID=%d) reading from named pipe:\n" % os.getpid())
        while True:
            line = r.readline()
            if line:
                print(line)
            else:
                break
        r.close()


def main():
    # This pipe works well communicating with processes in the same python file
    r, w = os.pipe()
    parent = os.fork()

    if parent:
        # Parent's sentences (PROCESS A)
        signal.signal(signal.SIGUSR2, pA_USR2_handler)
        child_pid = parent

        time.sleep(2)
        os.kill(child_pid, signal.SIGUSR1)

        signal.pause()
        # Process A reads the named pipe content after it receives a signal
        os.close(w)
        read_from_fifo(r)

        os.wait()
        os._exit(0)

    else:
        # Child's sentences (PROCESS B)
        signal.signal(signal.SIGUSR1, pB_USR1_handler)
        grandparent_pid = os.getppid()

        signal.pause()
        os.close(r)

        signal.signal(signal.SIGUSR1, pC_USR1_handler)

        child = os.fork()

        if child:
            # Child's sentences (PROCESS B)
            print("\n")
            message = "Message 1 (PID=" + str(os.getpid()) + ")"

            # Process B writes message 1 in named pipe
            with open(w, 'w') as w:
                w.write(message)
                w.flush()
            grandchild_pid = child

            time.sleep(1)
            os.kill(grandchild_pid, signal.SIGUSR1)

        else:
            # Grandchild's sentences (PROCESS C)
            signal.pause()
            print("\n")

            # Process C writes message 2 in named pipe
            message = "Message 2 (PID=" + str(os.getpid()) + ")"
            w = open(w)
            with os.fdopen(w, 'w') as w:
                w.write(message)
                w.close()
            print("todavia no envió a a buelo")
            # time.sleep(1)
            os.kill(grandparent_pid, signal.SIGUSR2)
            print("nieto envió a a buelo")

            os._exit(0)


if __name__ == '__main__':
    main()
