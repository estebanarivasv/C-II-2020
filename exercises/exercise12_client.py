import getopt
import sys

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


def execute_dgram_client(ip, port):
    import socket

    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    host = ip
    port = int(port)

    while True:
        msg = input('Enter message to send : ').encode()
        try:
            # Set the whole string
            clientsocket.sendto(msg, (host, port))

        except socket.error:
            print('Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()


def execute_stream_client(ip, port):
    import socket
    clientsocket = ""

    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print("Failed to create socket")

    host = ip
    port = int(port)

    clientsocket.connect((host, port))

    while True:
        try:
            msg = input("Enter message to send: ")
            clientsocket.send(msg.encode("ascii"))
        except EOFError:
            break

    print("\nClosing client...")
    clientsocket.close()


def main():
    port = ""
    ip = ""
    try:
        if len(sys.argv[1:]) <= 0:
            raise ValueError
        (option, value) = getopt.getopt(sys.argv[1:], "a:t:p:")
        print(option)
        for (opt, val) in option:
            if opt == "-p":
                port = val
            if opt == "-a":
                ip = val
        for (opt, val) in option:
            if opt == "-t":
                protocol = val.lower()
                if protocol == "udp":
                    print("Executing dgram client socket")
                    execute_dgram_client(ip, port)
                elif protocol == "tcp":
                    print("Executing stream client socket")
                    execute_stream_client(ip, port)
                else:
                    raise ValueError

    except ValueError or getopt.GetoptError:
        print("Usage: exercise12_server.py -p <port> -t <transport protocol> -f <text file route>")


if __name__ == '__main__':
    main()
