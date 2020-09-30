"""

--- Exercise statement: N°26 - Parallel squares (pool)

Reescriba el ejercicio 25 de manera que haga uso de Pools of workers.

Escriba dos versiones del programa:

- Una haciendo uso de la función map
- Una haciendo uso de la función apply

tag: [pool_cuad]

"""
import os
import getopt
import multiprocessing
import sys


def calc_square(i):
    print(f"Pool worker PID {os.getpid()} calculating...")
    return i * i


def split_list(range_list, wanted_parts=1):
    length = len(range_list)
    return [range_list[i * length // wanted_parts: (i + 1) * length // wanted_parts] for i in range(wanted_parts)]


if __name__ == "__main__":

    proc_num = 0
    min_number = 0
    max_number = 0

    if len(sys.argv[1:]) < 1:
        print("\nUsage:\n\tpython3 exercise25_parallel_squares.py -p <num_proc> -n <num_max> -m <num_min>")
        sys.exit(0)

    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:m:n:')

    for (option, value) in opt:
        if option == "-p":
            proc_num = int(value)
        if option == "-m":
            min_number = int(value)
        if option == "-n":
            max_number = int(value)

    pool = multiprocessing.Pool()

    values_range = list(range(min_number, max_number))
    proc_lists = split_list(values_range, proc_num)

    iterat = 1
    for values in proc_lists:
        map_result = (pool.map(calc_square, values))
        print(f"Iteration {iterat} result con map: {map_result}")
        iterat += 1
    print("")

    iterat = 1
    for values in proc_lists:
        apply_result = [pool.apply(calc_square, args=(i,)) for i in values]
        print(f"Iteration {iterat} result con apply: {apply_result}")
        iterat += 1

    pool.close()
