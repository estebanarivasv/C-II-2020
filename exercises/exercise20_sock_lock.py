"""

--- Exercise statement: N°20 - Lock/RLock (multiprocessing)

Escriba un servidor tcp que atienda un puerto pasado por argumento (-p en getopt), y
reciba los siguientes comandos: ABRIR, CERRAR, AGREGAR, y LEER, por parte de los clientes.

Si el cliente envía un comando ABRIR, el servidor deberá solicitarle un nombre de archivo.
Si el cliente envía un comando "AGREGAR" el servidor deberá solicitarle una cadena de texto
para agregar al final del archivo.
Si el cliente envía un comando "LEER" el servidor le deberá enviar al cliente el
contenido del archivo.
Si el cliente envía un comando "CERRAR" el servidor deberá cerrar el archivo y cerrar
la comunicación con el cliente.
El servidor deberá poder mantener conexiones en simultáneo con varios clientes mediante
un sistema multiproceso.
Deberá controlar el acceso concurrente en la escritura al archivo, de modo que no se
sobreescriban las escrituras de dos clientes en el mismo instante de tiempo.

tag: sock_lock

"""

import multiprocessing
import getopt
import sys
import socket
from ctypes import c_char_p


def shell(client_sock, address):

    manager = multiprocessing.Manager()

    print(f"\nGot a connection from {str(address)}.")

    file_route = manager.Value(c_char_p, "/tmp/file.txt")

    while True:
        msg = "Comandos:\n - ABRIR\n - AGREGAR\n - LEER\n - CERRAR\n - SALIR\n\n"
        client_sock.send(msg.encode())

        response = client_sock.recv(1024)
        if response.decode() == "ABRIR\r\n":
            message = "\nEnter file source: "
            client_sock.send(message.encode())
        elif response.decode() == "AGREGAR\r\n":
            message = "\nEnter string to append: "
            client_sock.send(message.encode())
            reply = client_sock.recv(1024)


            with open(file_route.value, "a") as file:
                file

        elif response.decode() == "LEER\r\n":
            with open(file_route.value, "r") as file:
                lines = file.readlines()
            message = "\nFile content: \n"
            for line in lines:
                message = message + line
            client_sock.send(message.encode())
        elif response.decode() == "CERRAR\r\n":
            break
        else:
            message = "\nCommand entered not valid. Exiting..."
            client_sock.send(message.encode())
            break



def start_stream_socket(server_port):
    host = ""

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Failed to create socket")
        sys.exit()

    server.bind((host, int(server_port)))
    server.listen(5)

    while True:
        client, addr = server.accept()
        client_shell = multiprocessing.Process(target=shell, args=(client, addr))
        client_shell.start()


if __name__ == '__main__':
    port = 0

    if len(sys.argv[1:]) <= 1:
        print("Usage: python ex20.py -p <port>")
    else:
        option, value = getopt.getopt(sys.argv[1:], "p:")
        for opt, val in option:
            if opt == "-p":
                port = val

        start_stream_socket(port)
