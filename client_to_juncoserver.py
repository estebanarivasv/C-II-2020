import socket
import sys	#for exit
import getopt

def sendMessage():
    msg = input("Message to send: ")
    s.send(msg.encode('ascii'))

def sendNextMessage():
    msg = input("Insert next message: ")
    s.send(msg.encode('ascii'))

def resendMessage():
    msg = input("Resend last message: ")
    s.send(msg.encode('ascii'))

def everythingOk():
    msg = s.recv(1024)
    msg.decode("ascii")
    print("Server response: ", msg)
    if msg == 400 or msg == 500:
        print("Try again")
        return False
    elif msg == 200:
        print("Everything ok")
        return True

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

# pyhton client_dgram.py ip_server puerto_server
(opts, args) = getopt.getopt(sys.argv[1:], "h:p:")
print(opts)
for (opt, arg) in opts:
    if opt == "-h":
        host = arg
    if opt == "-p":
        port = int(arg)

s.connect((host,port))

sendMessage()
for i in range(3):
    if everythingOk:
        sendNextMessage()
    elif not everythingOk:
        resendMessage()
print("Sending successful")
