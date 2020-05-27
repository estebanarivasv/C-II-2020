import socket
import sys	#for exit
import getopt

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

hello = "hello|" + (input('Enter name: '))
print(hello)
s.send(hello.encode('ascii'))
msg = s.recv(1024)
print('Server reply : ' + msg.decode("ascii"))

email = "email|" + (input('Enter email: '))+ "|"
print(email)
s.send(email.encode('ascii'))
msg = s.recv(1024)
print('Server reply : ' + msg.decode("ascii"))

key = "key|" + (input('Enter key: ')) + "|"
s.send(key.encode('ascii'))
msg = s.recv(1024)
print('Server reply : ' + msg.decode("ascii"))

exit = "exit"
s.send(exit.encode('ascii'))
msg = s.recv(1024)
print('Server reply : ' + msg.decode("ascii"))

