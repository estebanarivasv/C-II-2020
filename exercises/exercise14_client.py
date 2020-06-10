"""

--- Exercise statement: N°14 - remote shell

Reescribir el ejercicio anterior de modo que permita recibir consultas desde varios clientes remotos en forma
simultánea. Utilice el módulo multiprocessing de Python3 para lograr su objetivo.

Tag: remote_shell_multiproc

"""
import socket
import sys
import getopt
import datetime

if __name__ == '__main__':

    (option, value) = getopt.getopt(sys.argv[1:], "l:")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    host = "0.0.0.0"
    port = 5300

    s.connect((host, port))

    print("COMMAND PROMPT\n")
    while True:
        msg = input('Command: ')
        s.send(msg.encode('ascii'))

        msg = s.recv(1024)

        print('Server reply: ' + msg.decode("utf-8"))

        for (opt, val) in option:
            if opt == "-l":

                file_path = val

                file = open(str(file_path), "a")

                datetime_today = datetime.datetime.today()

                file.writelines("\n\n\n" + str(datetime_today) + "\n" + msg.decode("utf-8"))

                file.close()





