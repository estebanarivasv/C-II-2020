#!/usr/bin/python3
import socket, sys, time

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

# get local machine name
#host = socket.gethostname()                           
host = ""
port = int(sys.argv[1])

# bind to the port
serversocket.bind((host, port))                                  

while True:
    # establish a connection
    data,addr = serversocket.recvfrom(1024)
    print(addr)
    address = addr[0]
    port = addr[1]
    print("Address: %s - Port %d" % (address, port))
    print("Recibido: "+data.decode("ascii"))
    msg = input('Enter message to send : ').encode()
    serversocket.sendto(msg, addr)
    time.sleep(1)


clientsocket.close()


"""
Conectar al cliente usando ncat:
    ncat 127.0.0.1 1234 -u -v
"""

