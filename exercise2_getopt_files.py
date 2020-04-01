#!/usr/bin/python
import sys
import getopt

"""

--- Exercise statement: N°2 - Getopt - Files

If wanted, you can look in the examples folder /practice-excercises/python/argv

Escribir un programa que reciba dos nombres de archivos por línea de órdenes utilizando los parámetros “-i” y “-o” 
procesados con getopt().

El programa debe verificar que el archivo pasado a “-i” exista en el disco. De ser así, lo
abrirá en modo de solo lectura, leerá su contenido, y copiará dicho contenido en un
archivo nuevo cuyo nombre será el pasado a “-o”. Si el archivo nuevo ya existe, deberá
sobreescribirlo.

"""


def verify_existence(i_file):
    try:
        f = open(i_file)
        print("The file exists. Copying.")
    except IOError:
        print("The file either doesn't exist or it isn't accessible")
        sys.exit()


def main():
    try:
        if len(sys.argv[1:]) > 4:
            print("You've inserted more arguments than expected.")
        else:
            (opts, args) = getopt.getopt(sys.argv[1:], "i:o:")

            for (op, arg) in opts:
                if op == '-i':
                    print(arg)
                    verify_existence(arg)
                    f = open(arg, "r")
                    i_lines = f.readlines()

            for (op, arg) in opts:
                if op == '-o':
                    output_file = arg
                    o = open(output_file, "w")
                    o.writelines(i_lines)

    except getopt.GetoptError as err:
        print(str(err))
        sys.exit()

    print("Done!")
    sys.exit()


if __name__ == "__main__":
    main()
