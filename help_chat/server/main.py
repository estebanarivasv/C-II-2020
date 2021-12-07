import getopt
import multiprocessing
import socket
import sys

 
def interact_with_client():
    while True:
        data, addr = s.recvfrom(1024)
        address = addr[0]
        port = addr[1]
        print(f"Address: {address} - Port: {port}")

        msg_from_client = data.decode("ascii")
        print("<- ", msg_from_client)

        if data == "" or len(data) == 0:
            break

    print("Closing server...")
    s.close()


if __name__ == '__main__':

    host = ""  # INADDR_ANY, which is used to bind to all interfaces
    port = None

    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'p:', ['port='])
        if len(opts) != 4:
            print('Please check the options again.')
            sys.exit(0)

        for (op, arg) in opts:
            if op == '-p' or op == '--port':
                port = int(arg)
            else:
                print(f'Please check the options again.')
                sys.exit(0)

    except getopt.GetoptError:
        print("Usage: servidor/main.py -p <port>")

    if port is None:
        print('Please check the options again.')

    # DEFINE SOCKET
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    # TODO: Add clients multiprocessing or multithreading
    print('Connecting...\n')
    s.bind((host, port))

    print(f'Help chat server now working\n')

    while True:
        c, ip = s.accept()
        client = multiprocessing.Process(target=hash_parser, args=(c, ip))
        client.start()
