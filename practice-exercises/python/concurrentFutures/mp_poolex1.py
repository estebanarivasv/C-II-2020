import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main1():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

def main2():
    executor=concurrent.futures.ProcessPoolExecutor()
    for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
        print('%d is prime: %s' % (number, prime))


if __name__ == '__main__':
    main1()
    print("Main2 -------------------------------")
    main2()




"""
map() mapea en el pool la función con cada uno de los elementos de la lista
    retorna los resultados en el orden en que fueron pasados al iterable
    a diferencia del as_complete, que retorna el primer resultado que fue calculado
"""
