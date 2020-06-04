import getopt
import sys
import os

"""

--- Exercise statement: N°12 - stdin + sockets

Escriba un programa cliente-servidor con sockets que tenga el siguiente comportamiento.

    El usuario ejecutará el programa servidor pasándole tres argumentos:
        -p: El puerto en el que va a atender el servicio (por defecto debe atender en todas las direcciones
         de red configuradas en el sistema operativo).
        -t: Permitirá especificar el protocolo de transporte a utilizar. Las opciones válidas serán tcp 
        o udp.
        -f: Una ruta a un archivo de texto en blanco.
    El servidor creará el socket con los datos especificados, y creará, si no existe, el archivo de 
    texto.
    El cliente recibirá tres argumentos por línea de comandos:
        -a: La dirección IP del servidor
        -p: El puerto en el que atiende el servidor
        -t: El protocolo de transporte a usar. Por supuesto, para establecer la conexión correctamente 
        ambos, cliente y servidor, deberán especificar el mismo protocolo de transporte.
    El cliente comenzará a leer desde STDIN texto hasta que el usuario presione Ctrl+d.
    El cliente enviará todo el contenido por el socket al servidor.
    El servidor leerá todo el contenido desde el socket hasta que encuentre un EOF.
    El servidor almacenará todo el contenido en el archivo de texto creado.

NOTA: los parámetros serán pasados por argumento y parseados usando getopt.

Ejemplo de carga del servidor:

python3 servidor.py -p 1234 -t tcp -f /tmp/archivo.txt

Ejemplo de carga del cliente:

python3 cliente.py -a 192.168.0.23 -p 1234 -t tcp

Tag: tcp_udp

"""


def execute_dgram_server(port, route):
    import socket

    try:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    except socket.error:
        print("Failed to create socket")
        sys.exit()

    host = ""
    port = int(port)

    serversocket.bind((host, port))

    while True:
        data, addr = serversocket.recvfrom(1024)
        address = addr[0]
        port = addr[1]
        print("Address: %s - Port %d" % (address, port))
        print("Recibido: " + data.decode("ascii"))

        if os.path.exists(route):
            pass
        else:
            os.mknod(route)

        if data == "" or len(data) == 0:
            break
        else:
            file = open(route, "a")
            file.write(data.decode("ascii") + "\n")
            file.close()
    print("Closing server...")
    serversocket.close()


def execute_stream_server(port, route):
    import socket

    try:
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    except socket.error:
        print("Failed to create socket")
        sys.exit()

    host = ""
    port = int(port)

    serversocket.bind((host, port))

    serversocket.listen(1)

    clientsocket, address = serversocket.accept()

    while True:
        data, addr = clientsocket.recvfrom(1024)
        print(f"Address: {address[0]} - Port {address[1]}")
        print("Recibido: ", data.decode("ascii"))

        if os.path.exists(route):
            pass
        else:
            os.mknod(route)

        if data == "" or len(data) == 0:
            break
        else:
            file = open(route, "a")
            file.write(data.decode("ascii") + "\n")
            file.close()
    print("Closing server..")
    serversocket.close()




def main():
    port = ""
    route = ""
    try:
        if len(sys.argv[1:]) <= 0:
            print("Usage: exercise12_stdin_sockets_server.py -p <port> -t <transport protocol> -f <text file route>")
        (option, value) = getopt.getopt(sys.argv[1:], "p:t:f:")
        for (opt, val) in option:
            if opt == "-p":
                port = val
            if opt == "-f":
                route = val
        for (opt, val) in option:
            if opt == "-t":
                protocol = val.lower()
                if protocol == "udp":
                    print("Executing dgram server socket")
                    execute_dgram_server(port, route)
                elif protocol == "tcp":
                    print("Executing stream server socket")
                    execute_stream_server(port, route)
                else:
                    raise ValueError

    except getopt.GetoptError:
        print("Usage: exercise12_stdin_sockets_server.py -p <port> -t <transport protocol> -f <text file route>")


if __name__ == '__main__':
    main()
