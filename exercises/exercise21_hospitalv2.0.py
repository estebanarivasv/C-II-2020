"""

--- Exercise statement: N°21 - Sala de espera

Versión 1.0:

Simule una administración simple de una sala de espera de un hospital mediante Semáforos en multiproceso. Imagine que en
el hospital hay 5 consultorios atendiendo, y las personas van llegando en cada t segundos, siendo t un valor
aleatorio entre 1 y 3. Los médicos demoran un tiempo aleatorio entre 5 y 7 segundos en liberar a cada paciente. Los
pacientes van siendo atendidos en orden aleatorio, no necesariamente en el orden en el que llegan a la sala de
espera. El programa debe mostrar cuando un paciente llega al hospital, cuando es atendido, cuando se va,
y en cada operación debe mostrar la cantidad de consultorios libres.

Versión 2.0:

Haga uso de getopt para parametrizar la cantidad de consultorios del hospital, los tiempos mínimo y máximo en que
llegan las personas, y los tiempos mínimo y máximo en que un médico atiende a su paciente.

tag: hosp

"""

import multiprocessing
import random
import string
import time
import getopt
import sys


def getsChecked(c, p_id, doc_time):

    (min_d, max_d) = doctor_time

    # Doctor's patient release time
    release_time = random.randint(min_d, max_d)

    print(f"\n >>> Patient {p_id} arrives at the hospital. Available consulting rooms: {c.get_value()}")
    c.acquire()
    print(f"\n --> Patient {p_id} is now entering doctor's consulting room. Available consulting rooms: {c.get_value()}")
    time.sleep(release_time)
    c.release()
    print(f"\n <<< Patient {p_id} is leaving the hospital. Available consulting rooms: {c.get_value()}")


def generatesPeopleArriving(consulting_rooms, pt, dt):
    while True:
        # Patient arrival time
        arrival_time = random.randint(pt[0], pt[1])
        time.sleep(arrival_time)

        patient_id = random.choice(string.ascii_uppercase)
        patient_arriving = multiprocessing.Process(target=getsChecked, args=(consulting_rooms, patient_id, dt))
        patient_arriving.start()


if __name__ == '__main__':
    if len(sys.argv[1:]) <= 1:
        print("Usage:\n   python3 exercise21_hospitalv2.0.py"
              "\n -c <max_consulting_rooms>"
              "\n -k <min_people_arrival_time>"
              "\n -l <max_people_arrival_time>"
              "\n -m <min_doctor_release_time>"
              "\n -n <max_doctor_release_time>"
              "\n")

    else:
        (option, value) = getopt.getopt(sys.argv[1:], "c:k:l:m:n:")

        max_consul_rooms = 5
        min_people = 1
        max_people = 3
        min_doctor = 5
        max_doctor = 7

        for (opt, val) in option:
            if opt == "-c":
                max_consul_rooms = int(val)
            if opt == "-k":
                min_people = int(val)
            if opt == "-l":
                max_people = int(val)
            if opt == "-m":
                min_doctor = int(val)
            if opt == "-n":
                max_doctor = int(val)

        people_time = [min_people, max_people]
        doctor_time = [min_doctor, max_doctor]

        # Consulting rooms number
        consul_rooms = multiprocessing.Semaphore(5)

        hospital = multiprocessing.Process(target=generatesPeopleArriving, args=(consul_rooms, people_time, doctor_time))
        hospital.start()
