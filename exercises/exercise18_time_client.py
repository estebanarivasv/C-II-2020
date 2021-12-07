"""

--- Exercise statement: N°18 - time client

El protocolo time es un protocolo que utilizan los sistemas operativos para mantenerse sincronizados.

El funcionamiento es muy básico. El cliente consulta a un servidor de tiempo, y el servidor le envía el tiempo
UTC actual.

El servidor en general funciona en el puerto 37 tanto en UDP como en TCP. Para detalles de su funcionamiento
revisar la RFC 868 (https://tools.ietf.org/html/rfc868).

Algunos servidores atienden en puertos alternativos, por ejemplo:

diego@cryptos:tmp$ telnet time.nist.gov 13
Trying 132.163.96.4...
Connected to time.nist.gov.
Escape character is '^]'.

59073 20-08-12 00:14:45 50 0 0 534.4 UTC(NIST) *
Connection closed by foreign host.


Escribir un cliente en Python que conecte a un servidor time y muestre la hora actual en tiempo UTC.

Usar getopt para leer argumentos por línea de comandos:

-h host_servidor_time
-p puerto
-t tcp/udp
Ejemplo de ejecución:

./cliente_time.py -h time.nist.gov -p 13 -t tcp
Fecha y hora actual (UTC): 20-08-12 00:14:45
Tag: time

"""

import socket
import sys
import getopt


def run_client_dgram(udp_ip, udp_port):
    try:
        client_dgram = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    # Send an empty datagram
    client_dgram.sendto("".encode(), (udp_ip, udp_port))

    # Receive the time datagram
    data, addr = client_dgram.recvfrom(1024)  # buffer size is 1024 bytes
    try:
        print(f"Time:\n{data.decode()}")
    except UnicodeDecodeError:
        print("Error at decoding server response")


def run_client_stream(tcp_ip, tcp_port):
    try:
        client_stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    # Connect to port
    client_stream.connect((tcp_ip, tcp_port))

    # Receive the time
    time = client_stream.recv(1024).decode()

    try:
        print(f"Time:\n{time}")
    except UnicodeDecodeError:
        print("Error at decoding server response")


if __name__ == '__main__':

    (option, value) = getopt.getopt(sys.argv[1:], "h:p:t:")

    if len(sys.argv[1:]) <= 1:
        print("Usage: -h server_ip, -p server_port -t tcp/udp protocol\nExample: python3 exercise18_time_client.py -h "
              "time.nist.gov -p 13 -t tcp")
    else:
        host = ""
        port = ""
        protocol = ""

        for (opt, val) in option:
            if opt == "-p":
                port = int(val)
            if opt == "-h":
                host = val
            if opt == "-t":
                protocol = val.lower()

        if protocol == "tcp":
            run_client_stream(host, port)
        elif protocol == "udp":
            run_client_dgram(host, port)
        else:
            print("You have not introduced the required arguments.")
