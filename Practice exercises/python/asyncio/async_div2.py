import asyncio

async def encontrar_divisibles(rango, div_por):
    print("Buscando numeros en el rango {} divisibles por {}".format(rango, div_por))
    located = []
    for i in range(rango):
        if i % div_por == 0:
            located.append(i)
        if i % 50000 == 0:
            await asyncio.sleep(0.0001)

    print("Listo con nums en el rango {} divisibles por {}".format(rango, div_por))
    return located


async def main():
    divs1 = loop.create_task(encontrar_divisibles(5080000, 34113))
    divs2 = loop.create_task(encontrar_divisibles(1000520, 3210))
    divs3 = loop.create_task(encontrar_divisibles(500, 3))
    await asyncio.wait([divs1,divs2,divs3])
    return divs1, divs2, divs3


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.set_debug(1)
        d1, d2, d3 = loop.run_until_complete(main())
    #    print(d1.result())
    except Exception as e:
        # logging...etc
        pass
    finally:
        loop.close()
