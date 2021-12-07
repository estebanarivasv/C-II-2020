"""

--- Exercise statement: N°11 - socket streams

El código server_compu2.py (repo git de la cátedra) implementa un protocolo que corre sobre TCP y
tiene los siguientes comandos:

hello|<nombre>
email|<correo_electronico>
key|<clave_hardodeada> # Compu2_2020
exit


Estos comandos deben ser enviados al servidor en ese mismo orden, y por cada uno el servidor 
responderá con uno de los siguientes códigos:

    200: OK
    400: Comando válido, pero fuera de secuencia.
    500: Comando inválido.
    404: Clave errónea.
    405: Cadena nula.

Al obtener un valor distinto de 200 el servidor seguirá esperando el valor correcto en el siguiente intento,
por lo que no será necesario reiniciar la conexión.

Programe un cliente TCP que pueda conectar contra el servidor pidiéndole al usuario los datos uno por uno,
y analizando las respuestas desde el servidor para notificar al cliente ante cualquier problema.

La salida del servidor, en el caso de haber llevado a cabo todos los pasos correctamente, será algo
similar a esto:

27-05-2020_19:39:16|diego|diego@juncotic.com|Compu2_2020|('127.0.0.1', 47980)
"""

import socket
import sys
import getopt


def main():
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    (opts, args) = getopt.getopt(sys.argv[1:], "h:p:")
    for (opt, arg) in opts:
        if opt == "-h":
            host = arg
        if opt == "-p":
            port = int(arg)

    c.connect((host, port))

    for i in range(4):
        msg_to_send = input("Message to send: ")
        c.send(msg_to_send.encode('ascii'))

        test_msg = True

        while test_msg:
            msg_received = c.recv(1024)
            msg_received.decode("ascii")
            print("Server response: ", msg_received)

            if msg_received == b'400' or msg_received == b'404' or msg_received == b'405' or msg_received == b'500':
                print("Please, change the sentence")
                msg_to_send = input("Message to send: ")
                c.send(msg_to_send.encode('ascii'))

            elif msg_received == b'200':
                print("Everything OK.")
                test_msg = False
    c.close()


if __name__ == '__main__':
    main()
