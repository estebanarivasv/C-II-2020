"""

--- Exercise statement: N°22 - Walkie-Talkie

Escribir dos programas que interactúen entre si como si fuesen clientes peer-to-peer. El funcionamiento será el
siguiente:

Llamemos Alice al primer programa en ejecutarse, y Bob al segundo.

Alice quedará escuchando un texto desde el otro programa.

Bob permitirá al usuario escribir por entrada estándar un mensaje. Al dar enter se enviará dicho mensaje a Alice,
que lo mostrará por pantalla. Este paso se repetirá hasta que Bob envíe un mensaje con el texto “cambio”. En ese
momento Bob comenzará a escuchar desde el proceso Alice.

Alice al recibir la palabra “cambio”, permitirá al usuario escribir texto por línea de comandos. Al dar enter los
mensajes viajarán hasta Bob, que los mostrará por pantalla. Cuando Alice envíe un texto “cambio”, se invertirá
nuevamente la secuencia.

Cuando cualquiera de los dos procesos envíe “exit” terminarán ambos.

Utilice Sockets Inet Stream para comunicar ambos procesos.

tag: walkie
"""
import socket
import sys
import os
import getopt
import time


def send(cl_socket):
    goodbye = "over and out"
    while True:
        msg = input("\nMessage to Bob: ")
        if msg.lower() == goodbye:
            cl_socket.send(msg.encode())
            time.sleep(2)
            break
        else:
            cl_socket.send(msg.encode())


def receive(cl_socket):
    goodbye = "over and out"
    while True:
        data = cl_socket.recv(1024).decode()
        if data.lower() != goodbye:
            print(f"\n>>> Bob says: {data}")
        else:
            time.sleep(2)
            break


def walkie_talkie(client_socket, address):
    print(f"\nGot a connection from {str(address)}.")
    while True:
        receive(client_socket)
        send(client_socket)


if __name__ == '__main__':
    if len(sys.argv[1:]) <= 1:
        print("Usage:\n   python3 exercise22_alice.py -p <port>")
    else:
        host = ""
        port = 0

        (option, value) = getopt.getopt(sys.argv[1:], "p:")
        for (opt, val) in option:
            if opt == "-p":
                port = int(val)
        try:
            s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            sys.exit()

        s_socket.bind((host, port))
        s_socket.listen(5)  # Accepts 5 connections max from clients
        
        c_socket, addr = s_socket.accept()

        walkie_talkie(c_socket, addr)
