"""
This script was written by @d1cor

"""


#!/usr/bin/python3
import socket, os, threading, datetime

MAX_SIZE=512
KEY="Compu2_2020"

TODAY=datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")


def th_server(sock_full):
    name = "_"
    key="_"
    email="_"
    sock,addr = sock_full
    print("Launching thread... addr: %s" % str(addr))
    exit = False
    ip=str(addr)
    stage = 0
    while True:
        msg = sock.recv(MAX_SIZE).decode()
        msg = msg.replace('\n', '').replace('\r', '')
#        print("Recibido: %s" % msg)
        if msg[0:5] =="hello": 
            if stage == 0:
                name = msg[6:]
                if len(name)==0:
                    resp="405"
                else:
                    resp = "200"
                    stage += 1
            else:
                resp = "400"
        elif msg[0:5] == "email":
            email = msg[6:]
            if stage==1:
                if len(email)==0:
                    resp="405"
                else:
                    email = msg[6:]
                    resp = "200"
                    stage+=1
            else:
                resp = "400"
        elif msg[0:3] == "key":
            if stage==2:
                key = msg[4:]
                if key != KEY:
                    resp="404"
                else:
                    resp = "200"
                    stage+=1
            else:
                resp = "400"
        elif msg[0:4] == "exit":
            resp = "200"
            exit = True
        else:
            resp = "500"

        sock.send(resp.encode("ascii"))
        if exit:
            data = "%s|%s|%s|%s|%s" % (TODAY,name,email,key,ip)
            print(data)
            sock.close()
            break
            




# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
#host = socket.gethostname()
host = ""
port= 8000

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)

while True:
    # establish a connection
    clientsocket = serversocket.accept()

    print("Got a connection from %s" % str(clientsocket[1]))
    th = threading.Thread(target=th_server, args=(clientsocket,))
    th.start()

