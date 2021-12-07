#!/usr/bin/python
import sys
import getopt

"""
--- Exercise statement: N°1 - Getopt - Calculator

If wanted, you can look in the examples folder /practice-excercises/python/argv

Crear una calculadora, donde se pase como argumentos luego de la opción -o el
operador que se va a ejecutar (+,-,*,/), luego de -n el primer número de la operación,de -m el segundo número.
Ejemplo:
            ./calc -o + -n 5 -m 6
            5 + 6 = 11
Considerar que el usuario puede ingresar los argumentos en cualquier orden. El programa deberá verificar que los
argumentos sean válidos (no repetidos, números enteros, y operaciones válidas.

"""


def main():
    first_num = 0
    second_num = 0
    try:
        if len(sys.argv[1:]) > 6:
            print("You've inserted more arguments than expected for the calculator.")
            sys.exit()
        else:
            (opts, args) = getopt.getopt(sys.argv[1:], "o:n:m:")
        """Gets the arguments with the options -o (something), -n (something), -n (something)"""
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit()

    for (op, arg) in opts:
        if op == '-n':
            try:
                first_num = int(arg)
            except ValueError:
                print("The first number is not an integer.")
                sys.exit()

        if op == '-m':
            try:
                second_num = int(arg)
            except ValueError:
                print("The second number is not an integer.")
                sys.exit()

    for (op, arg) in opts:
        if op == '-o':
            if arg == '+':
                print(first_num, " + ", second_num, " =", first_num + second_num)
            elif arg == 'x':
                print(first_num, " x ", second_num, " =", first_num * second_num)
            elif arg == '-':
                print(first_num, " - ", second_num, " =", first_num - second_num)
            elif arg == '/':
                try:
                    print(first_num, " / ", second_num, " =", first_num / second_num)
                except ZeroDivisionError:
                    print("Division by zero is undefined.")
                    sys.exit()
            else:
                print("You haven't entered a valid operation")
                sys.exit()


if __name__ == "__main__":
    main()

