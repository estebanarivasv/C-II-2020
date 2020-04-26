import sys
import getopt
import os

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





def main():
    (opts, args) = getopt.getopt(sys.argv[1:], 'p:', ['process='])
    for option, value in opts:
        if option == "--process" or option == "-p":
            childs_num = value

            for i in range(childs_num):
                new_child = os.fork()



if __name__ == '__main__':
    main()