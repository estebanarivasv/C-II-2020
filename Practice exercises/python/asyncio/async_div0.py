def encontrar_divisibles(rango, div_por):
    print("Buscando numeros en el rango {} divisibles por {}".format(rango, div_por))
    located = []
    for i in range(rango):
        if i % div_por == 0:
            located.append(i)
    print("Listo con nums en el rango {} divisibles por {}".format(rango, div_por))
    return located

def main():
    divs1 = encontrar_divisibles(50800000, 34113)
    divs2 = encontrar_divisibles(10005200, 3210)
    divs3 = encontrar_divisibles(500, 3)


if __name__ == '__main__':
    main()
