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


def getsChecked(c, id):
    # Doctor's patient release time
    release_time = random.randint(5, 7)

    print(f"\n >>> Patient {id} arrives at the hospital. Available consulting rooms: {c.get_value()}")
    c.acquire()
    print(f"\n --> Patient {id} is now entering doctor's consulting room. Available consulting rooms: {c.get_value()}")
    time.sleep(release_time)
    c.release()
    print(f"\n <<< Patient {id} is leaving the hospital. Available consulting rooms: {c.get_value()}")


def generatesPeopleArriving(consulting_rooms):
    while True:
        # Patient arrival time
        arrival_time = random.randint(1, 3)

        time.sleep(arrival_time)

        patient_id = random.choice(string.ascii_uppercase)
        patient_arriving = multiprocessing.Process(target=getsChecked, args=(consulting_rooms, patient_id))
        patient_arriving.start()


if __name__ == '__main__':
    # Consulting rooms number
    consul_rooms = multiprocessing.Semaphore(5)

    hospital = multiprocessing.Process(target=generatesPeopleArriving, args=(consul_rooms,))
    hospital.start()
