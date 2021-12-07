import getopt
import socket
import sys

if __name__ == '__main__':

    host = None
    port = None
    department = None
    role = None

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'h:p:d:r:', ['host=', 'port=', 'department=', 'role='])
        if len(opts) != 4:
            print('Please check the options again.')
            sys.exit(0)

        for (op, arg) in opts:
            if op == '-h' or op == '--host':
                host = str(arg)
            elif op == '-p' or op == '--port':
                port = int(arg)
            elif op == '-d' or op == '--department':
                department = str(arg)
            elif op == '-r' or op == '--role':
                role = str(arg)
            else:
                raise getopt.GetoptError
            for i in [host, port, department, role]:
                if i is None:
                    raise getopt.GetoptError

    except getopt.GetoptError:
        print("Usage: cliente/main.py -h <host> -p <port> -d <department> -r <role>")
        sys.exit(0)

    # todo: delete this
    print(host, port, department, role)

    # DEFINE SOCKET
    print('Connecting...\n')
    try:
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Socket error', e)
        sys.exit()

    c.connect((host, port))

    print('\nConnected to "Sumamos" help chat\n')
    while True:
        msg_to_server = input("-> ").encode('ascii')
        c.send(msg_to_server)

        msg_from_server = c.recv(1024).decode('ascii')

        print("<- " + msg_from_server)

        # todo: handle logging in order to skip "department" and "role"

        # todo: add socket closing at signal

        c.close()
