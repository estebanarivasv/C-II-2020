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


def walkie_talkie(client_socket, g_bye):
    while True:
        while True:
            msg = input("\nMessage to Alice: ")
            if msg == goodbye.upper() or msg == goodbye:
                break
            else:
                client_socket.send(msg.encode())

        while True:
            data = client_socket.recv(1024).decode()
            if data == goodbye.upper() or data == goodbye:
                break
            else:
                print(f"\n>>> Alice says: {data}")


if __name__ == '__main__':

    if len(sys.argv[1:]) <= 1:
        print("Usage:\n   python3 exercise22_bob.py -p <port>")
    else:
        (option, value) = getopt.getopt(sys.argv[1:], "p:")
        for (opt, val) in option:
            if opt == "-p":
                port = val
        try:
            c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            sys.exit()

        host = "0.0.0.0"
        port = 0

        c_socket.connect((host, port))

        goodbye = "over and out"
        walkie_talkie(c_socket, goodbye)
