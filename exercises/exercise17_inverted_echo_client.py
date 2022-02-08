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

if __name__ == '__main__':

    (option, value) = getopt.getopt(sys.argv[1:], "h:p:")

    if len(sys.argv[1:]) <= 1:
        print("Usage: -h server_ip, -p server_port")
    else:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            sys.exit()

        host = ""
        port = 0

        for (opt, val) in option:
            if opt == "-p":
                port = int(val)
            if opt == "-h":
                host = val

        s.connect((host, port))

        while True:
            msg = input('To server <<< ')
            s.send(msg.encode())

            msg = s.recv(1024)
            print('From server >>> ' + msg.decode())
