#!/usr/bin/python
import getopt
import sys
import subprocess as sp

"""

--- Exercise statement: N°3 - subprocess.Popen

If wanted, you can look in the examples folder /practice-excercises/python/proc

Escribir un programa que reciba por argumentos de línea de comandos los siguientes modificadores:

    -c command
    -f output_file
    -l log_file

El código deberá crear los archivos pasados por los argumentos -f y -l en el caso de que no existan.

El código deberá ejecutar el comando haciendo uso de subprocess.Popen, y almacenar su salida en el
archivo pasado en el parámetro -f. En el archivo pasado por el modificador -l deberá almacenar el
mensaje “fechayhora: Comando XXXX ejecutado correctamente” o en su defecto el mensaje de error generado
por el comando si este falla.

Por ejemplo:

python ejecutor.py -c "ip a" -f /tmp/salida -l /tmp/log

El archivo /tmp/salida deberá contener la salida del comando, y /tmp/log deberá contener:

fechayhora: Comando “ip a” ejecutado correctamente.

Otro ejemplo:

python ejecutor.py -c “ls /cualquiera” -o /tmp/salida -l /tmp/log

El archivo /tmp/salida no contendrá nada nuevo, ya que el comando fallará. El archivo /tmp/log contendrá:

fechayhora: ls: cannot access '/cualquiera': No such file or directory

Notas

    fechayhora debe ser la fecha y la hora del sistema en el momento de ejecutar el comando.
    Si los archivos ya tienen contenido, las nuevas ejecuciones agregarán mensajes al final de los mismos, 
sin limpiar salidas anteriores.
    Los mensajes de error almacenados en el log_file serán los mensajes que genera el comando en su intérprete de
comandos, no deberá generarlos el progama escrito en python.

"""


def get_command(opts):
    for i in opts:
        for (op, arg) in opts:
            if op == "-c":
                return arg


def get_log(opts):
    for i in opts:
        for (op, arg) in opts:
            if op == "-l":
                return arg


def get_out_file(opts):
    for i in opts:
        for (op, arg) in opts:
            if op == "-f":
                return arg


def main():
    (opts, args) = getopt.getopt(sys.argv[1:], "c:f:l:")
    command = get_command(opts)
    log = open(str(get_log(opts)), "a")
    out_file = open(str(get_out_file(opts)), "a")

    date_fn = sp.Popen(["date"], stdout=sp.PIPE, universal_newlines=True)
    date_stdout = str(date_fn.communicate()[0])

    main_fn = sp.Popen([command], shell=True, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
    fn_out, fn_err = main_fn.communicate()

    if len(str(fn_err)) == 0:
        print("Log:\n\n", date_stdout, "Command ", str(command), " properly executed.\n\n")
        log.writelines("\n" + date_stdout + "Command " + str(command) + " properly executed.\n\n")
        print("Output file:\n\n", date_stdout, fn_out)
        out_file.writelines("\n" + date_stdout + fn_out)
    else:
        print("Log:\n\n", date_stdout, fn_err)
        log.write(str("\n" + date_stdout + fn_err))


if __name__ == '__main__':
    main()
