from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
    print("Hijo recibiendo: "+conn.recv())
    conn.send("Hola padre... hora de morir xD")
    conn.close()

if __name__ == '__main__':
    a, b = Pipe()
    p = Process(target=f, args=(b,))
    p.start()
    print (a.recv())   # prints "[42, None, 'hello']"
    a.send("Hola hijo... I am your father...")
    print ("Padre recibiendo: %s" % a.recv())
    p.join()
    print("Hora de morir tambien... Bye... (x.x)")
