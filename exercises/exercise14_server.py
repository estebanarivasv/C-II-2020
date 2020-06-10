"""

--- Exercise statement: N°14 - remote shell

Reescribir el ejercicio anterior de modo que permita recibir consultas desde varios clientes remotos en forma
simultánea. Utilice el módulo multiprocessing de Python3 para lograr su objetivo.

Tag: remote_shell_multiproc

"""
import subprocess as sp
import socket
import sys
import getopt
import multiprocessing


def shell(c_socket, address):

    print(f"\nGot a connection from {str(address)}.")

    while True:
        data = c_socket.recv(1024)

        data.decode('ascii')

        print(data)

        data = str(data)

        if data == "\n":
            break

        print(f"\nAddress: {str(address)}")
        print(f"\nReceived: {data}")

        function = sp.Popen([data], shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)

        stdout, stderr = function.communicate()

        message = "\n\nSTDOUT: \n" + stdout + "\n\n" + "STDERR: \n" + stderr

        c_socket.send(message.encode('ascii'))


if __name__ == '__main__':

    (option, value) = getopt.getopt(sys.argv[1:], "l")

    for (opt, val) in option:
        if opt == "-l":
            port = val

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = ""
    port = 5300

    serversocket.bind((host, port))

    serversocket.listen(5)
    # Accepts 5 connections max from clients

    while True:

        clientsocket, addr = serversocket.accept()

        client = multiprocessing.Process(target=shell(clientsocket, addr))

        client.start()
