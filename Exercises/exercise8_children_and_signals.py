import sys
import getopt
import os
import signal
import time

"""

--- Exercise statement: N°8 - children and signals

Escribir un programa que genere N procesos hijos. N será un argumento pasado por línea de comandos mediante el
modificador “-p” o “--process” (ambas deben estar contempladas).

El proceso padre deberá mostrar un mensaje del estilo “Creando proceso: xxxx” al momento de crear cada uno de sus
procesos hijos.

El proceso padre, luego de crear los N hijos, enviará una señal a cada uno de ellos (SIGUSR2).

Cada hijo mostrará por pantalla, al recibir la señal, el mensaje: “Soy el PID xxxx, recibí la señal yyyy de mi padre
PID zzzz”, donde xxxx es el pid del hijo en cuestión, yyyy el número de señal, y zzzz el pid del proceso padre inicial.

Debe verificar que los PIDs mostrados por el padre coincidan con los pids mostrados por cada hijo, y por supuesto,
todos los hijos deberán ser del mismo padre.



"""


def send_signal(pid):
    pid = int(pid)
    os.kill(pid, signal.SIGUSR2)


def USR2_handler(s, frame):
    print("I'm process PID ", os.getpid(), ". I recieved the signal 12 (SIGUSR2) from my parent PID ", os.getppid())


def main():
    (opts, args) = getopt.getopt(sys.argv[1:], 'p:', ['process='])
    if len(opts) < 2:
        print("Usage: \nSpecify how many child processes you want to create with -p <num> or --process <num>")
    for option, value in opts:
        if option == "--process" or option == "-p":
            childs_num = int(value)

            for i in range(childs_num):
                new_child = os.fork()
                if new_child == 0:
                    signal.signal(signal.SIGUSR2, USR2_handler)
                    signal.pause()
                    os._exit(0)
                else:
                    time.sleep(0.1)
                    print("Creating process. PID: ", new_child)
                    send_signal(new_child)
                    os.wait()
                    print("Process creation successful.")


if __name__ == '__main__':
    main()
