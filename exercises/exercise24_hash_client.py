"""

--- Exercise statement: N°24 - Hash

Realizar un programa cliente-servidor en Python que permita calcular las funciones hash de un archivo pasado por
opciones de línea de comandos.

El servidor deberá atender en un puerto TCP determinado pasado por argumento -p.

El servidor recibirá conexiones desde clientes remotos, y deberá lanzar un proceso que atienda cada conexión si se lo
inicia con la opción “-m”, o un hilo si se hace con la opción “-t”.

El cliente recibirá las siguientes opciones por línea de comandos:

-a host
-p port
-c texto
-h hash_function

Donde hash_function podrá ser:

sha1sum
sha224sum
sha256sum
sha384sum
sha512sum
sha3-224sum
sha3-256sum
sha3-384sum
sha3-512sum
Un ejemplo de ejecución sería el siguiente:

Ejecución del servidor (modo multiprocessing):

./server.py -p 1234 -m
Ejecución cliente:

./cliente.py -a 192.168.0.112 -p 1234 -h sha256sum -c "hola mundo"
40b6ba3be46c03f4af4ebb5bdbc1cfee4da1ab6bd017b48f3d336aabdbcba6e0
Donde la cadena de caracteres representa el resumen sha256 de la cadena pasada por argumento -c.

tag: hash
"""
import socket
import sys
import getopt
import multiprocessing
import threading


def hash_parser(c_socket, address):
    print(f"\nGot a connection from {str(address)}.")
    while True:
        data = c_socket.recv(1024).decode()
        data = data.strip("|")
        print(data)

        # HASH TRANSLATION

        message = "HASH: "
        c_socket.send(message.encode())


if __name__ == '__main__':

    if len(sys.argv[1:]) <= 1:
        print("Usage:\n   python3 exercise24_hash_client.py -a <host> -p <port> -c <text> -h <hash type>")
    else:
        host = ""
        port = 0
        text = ""
        hash_type = ""

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print('Failed to create socket')
            sys.exit()

        (option, value) = getopt.getopt(sys.argv[1:], "a:p:c:h:")
        for (opt, val) in option:
            if opt == "-a":
                host = val
            if opt == "-p":
                port = int(val)
            if opt == "-c":
                text = val
            if opt == "-h":
                hash_type = val

        s.connect((host, port))

        to_hash = text + "|" + hash_type
        s.send(to_hash.encode())

        response = s.recv(1024)
        print(response.decode())

        s.close()
