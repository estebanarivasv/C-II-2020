"""

--- Exercise statement: N°13 - remote shell

Escriba un programa cliente/servidor en python que permita ejecutar comandos GNU/Linux en una computadora
remota.

Técnicamente, se deberá ejecutar un código servidor en un equipo “administrado”, y programar un cliente 
(administrador) que permita conectarse al servidor mediante sockets STREAM.

El cliente deberá darle al usuario un prompt en el que pueda ejecutar comandos de la shell.

Esos comandos serán enviados al servidor, el servidor los ejecutará, y retornará al cliente:

    la salida estándar resultante de la ejecución del comando
    la salida de error resultante de la ejecución del comando.

El cliente mostrará en su consola local el resultado de ejecución del comando remoto, ya sea que se haya 
realizado correctamente o no, anteponiendo un OK o un ERROR según corresponda.

Ejemplo de ejecución del cliente (la salida de los comandos corresponden a la ejecución en el equipo 
remoto.

diego@cryptos$ python3 ejecutor_cliente.py
> pwd
OK
/home/diego
> ls -l /home
OK
drwxr-xr-x 158 diego diego 20480 May 26 18:57 diego
drwx------   2 root  root  16384 May 28  2014 lost+found
drwxr-xr-x   6 andy  andy   4096 Jun  4  2015 user
> ls /cualquiera
ERROR
ls: cannot access '/cualquiera': No such file or directory
>

Agregue en el cliente la opción “-l <file>” para permitirle al usuario almacenar un log de toda la sesión 
(comandos ejecutados y su fecha/hora).

Tag: remote_shell

"""
import socket
import sys
import getopt
import datetime

if __name__ == '__main__':

    (option, value) = getopt.getopt(sys.argv[1:], "l:")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    host = "0.0.0.0"
    port = 5500

    s.connect((host, port))

    print("COMMAND PROMPT\n")
    while True:
        msg = input('Command: ')
        s.send(msg.encode('ascii'))

        msg = s.recv(1024)

        print('Server reply: ' + msg.decode("utf-8"))

        for (opt, val) in option:
            if opt == "-l":

                file_path = val

                file = open(str(file_path), "a")

                datetime_today = datetime.datetime.today()

                file.writelines("\n\n\n" + str(datetime_today) + "\n" + msg.decode("utf-8"))

                file.close()





