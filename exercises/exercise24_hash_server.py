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

"""
import socket
import sys
import getopt
import multiprocessing
import threading
import hashlib


def hash_generator(t, h):
    message = ""
    print(t)
    t = t.encode()
    if h == "sha1sum":
        message = "HASH: " + hashlib.sha1(t).hexdigest()
    elif h == "sha224sum":
        message = "HASH: " + hashlib.sha224(t).hexdigest()
    elif h == "sha256sum":
        message = "HASH: " + hashlib.sha256(t).hexdigest()
    elif h == "sha384sum":
        message = "HASH: " + hashlib.sha384(t).hexdigest()
    elif h == "sha512sum":
        message = "HASH: " + hashlib.sha512(t).hexdigest()
    elif h == "sha3-224sum":
        message = "HASH: " + hashlib.sha3_224(t).hexdigest()
    elif h == "sha3-256sum":
        message = "HASH: " + hashlib.sha3_256(t).hexdigest()
    elif h == "sha3-384sum":
        message = "HASH: " + hashlib.sha3_384(t).hexdigest()
    elif h == "sha3-512sum":
        message = "HASH: " + hashlib.sha3_512(t).hexdigest()
    else:
        message = "Unknown hash type. " \
                  "Supported: \nsha1sum\nsha224sum\nsha256sum\nsha384sum\nsha512sum" \
                  "\nsha3-224sum\nsha3-256sum\nsha3-384sum\nsha3-512sum"
    return message


def hash_parser(c_socket, address):
    print(f"\nGot a connection from {str(address)}.")

    data = c_socket.recv(1024).decode()
    data = data.split("|")
    text = str(data[0])
    print(text)
    hash_type = str(data[1]).lower()

    message = hash_generator(text, hash_type)
    c_socket.send(message.encode())


if __name__ == '__main__':

    if len(sys.argv[1:]) <= 1:
        print("Usage:\n   python3 exercise24_hash_server.py -p <port> <-m (multiprocessing), -t (threading)>")
    else:
        host = ""
        port = 0
        exec_type = ""

        (option, value) = getopt.getopt(sys.argv[1:], "p:mt")
        for (opt, val) in option:
            if opt == "-p":
                port = val
            if opt == "-m":
                exec_type = "mp"
            if opt == "-t":
                exec_type = "th"

        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serversocket.bind((host, int(port)))
        serversocket.listen(5)
        # Accepts 5 connections max from clients

        while True:
            clientsocket, addr = serversocket.accept()
            if exec_type == "mp":
                client = multiprocessing.Process(target=hash_parser, args=(clientsocket, addr))
                client.start()
            if exec_type == "th":
                client = threading.Thread(target=hash_parser, args=(clientsocket, addr))
                client.start()
