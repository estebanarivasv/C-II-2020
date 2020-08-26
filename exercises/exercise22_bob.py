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
import getopt
import time


def send(server_sock):
    goodbye = "over and out"
    while True:
        msg = input("\nMessage to Alice: ")
        if msg.lower() == goodbye:
            server_sock.send(msg.encode())
            time.sleep(2)
            break
        else:
            server_sock.send(msg.encode())
    while True:
        data = server_sock.recv(1024).decode()
        if data.lower() != goodbye:
            print(f"\n>>> Alice says: {data}")
        else:
            print(f"\n>>> Alice says: {data}")
            time.sleep(2)
            break


def walkie_talkie(server_socket):
    while True:
        send(server_socket)


if __name__ == '__main__':

    if len(sys.argv[1:]) <= 1:
        print("Usage:\n   python3 exercise22_bob.py -p <port>")
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

        s_socket.connect((host, port))

        walkie_talkie(s_socket)
