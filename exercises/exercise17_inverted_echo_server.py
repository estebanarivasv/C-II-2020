"""

--- Exercise statement: N°17 - echo invertido

Escribir un programa cliente-servidor de echo reverso, es decir, un servidor que quede atendiendo conexiones
en un puerto pasado por argumento (-p), y un cliente que conecte a dicho servidor.

El cliente deberá leer desde el stdin cadenas de caracteres, las enviará al servidor, y el servidor responderá
con la misma cadena en orden invertido, es decir, algo así:

./cliente -h 127.0.0.1 -p 1234
>> hola
--> aloh
>> que tal?
--> ?lat euq
Hacer uso de fork o multiprocessing para permitirle al servidor atender varios clientes simultaneamente.

Usar socket INET STREAM (TCP).

Leer los parámetros por línea de comandos (usar getopt.getopt):

Cliente:
    -h direccion_ip_servidor
    -p puerto_servidor
Servidor:
    -p puerto_servidor
    (atiende en todas las ip's locales (0.0.0.0)

Tag: echo_inv

"""

import socket
import sys
import getopt
import multiprocessing


def invert_char(c_socket, address):
    print(f"\nGot a connection from {str(address)}.")

    while True:
        data = c_socket.recv(1024)
        data = data.decode()
        if data == "\n":
            break

        reversed_string = data[::-1]
        c_socket.send(reversed_string.encode())


if __name__ == '__main__':

    (option, value) = getopt.getopt(sys.argv[1:], "p:")

    if len(sys.argv[1:]) <= 1:
        print("Usage: -p server_port")
    else:
        host = ""
        port = 0

        for (opt, val) in option:
            if opt == "-p":
                port = val

        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((host, int(port)))
        serversocket.listen(5)
        # Accepts 5 connections max from clients

        while True:
            clientsocket, addr = serversocket.accept()
            client = multiprocessing.Process(target=invert_char, args=(clientsocket, addr))
            client.start()
