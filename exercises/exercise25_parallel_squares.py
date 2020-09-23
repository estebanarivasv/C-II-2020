"""

--- Exercise statement: N°25 - Parallel squares

Realizar un programa en python que reciba por argumentos:

-p cantidad_procesos
-m num_min
-n num_max

El programa deberá recorrer el range(m,n) y para cada uno de los valores mostrar por pantalla el resultado de
calcular el cuadrado de cada uno de los valores del rango.

La ejecución deberá realizarse en paralelo haciendo uso de la cantidad de procesos pasados por argumento.

Un ejemplo de ejecución sería:

python3 pcuadrado.py -p 2 -m 4 -n 10

Esta ejecución deberá evaluar el cuadrado de los números (2, 3, 4, 5, 6, 7, 8, 9) utilizando dos procesos, es decir,
cada proceso calculará el cuadrado de la mitad de los valores de la lista. Por ejemplo, un proceso podría calcular el
cuadrado de (2,3,4,5) mientras el otro calcula el cuadrado de (6,7,8,9).

tag: [pcuadrado]
"""

import getopt
import multiprocessing
import sys
import threading
import time


def print_sol(pipe):
    while True:
        time.sleep(0.01)
        data = pipe.recv()
        if data == 404:
            print(f"Thread {multiprocessing.current_process().name} exiting...")
            break
        print(f"Thread {multiprocessing.current_process().name} got {data} from process.")
        pipe.send(f"OK  {data} {multiprocessing.current_process().name}")


def calculate_val(pipe, val_list):
    print(f"Process {threading.current_thread().getName()} achieving list {str(val_list)}")
    for i in val_list:
        pipe.send(i * i)
        print(f"Process {threading.current_thread().getName()} got process message: {pipe.recv()}")
        time.sleep(1)
    pipe.send(404)


def split_list(range_list, wanted_parts=1):
    length = len(range_list)
    return [range_list[i * length // wanted_parts: (i + 1) * length // wanted_parts] for i in range(wanted_parts)]


if __name__ == "__main__":

    proc_num = 0
    min_number = 0
    max_number = 0

    """
    -p cantidad_procesos
    -m num_min
    -n num_max
    """

    if len(sys.argv[1:]) < 1:
        print("\nUsage:\n\tpython3 exercise25_parallel_squares.py -p <num_proc> -n <num_max> -m <num_min>")
        sys.exit(2)

    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:m:n:')

    for (option, value) in opt:
        if option == "-p":
            proc_num = int(value)
        if option == "-m":
            min_number = int(value)
        if option == "-n":
            max_number = int(value)

    values_range = list(range(min_number, max_number))
    proc_lists = split_list(values_range, proc_num)

    for values in proc_lists:
        a, b = multiprocessing.Pipe()
        p = multiprocessing.Process(name="value calculator", target=calculate_val, args=(b, values))
        h = threading.Thread(name="solution printer", target=print_sol, args=(a,))
        p.start()
        h.start()
