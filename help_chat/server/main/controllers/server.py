import getopt
import multiprocessing
import signal
import socket
import sys

from main.views import ConsoleView
from main.services import ServerService

v = ConsoleView()


class ServerController:

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = None
        self.server_serv = ServerService()

    def load_connection_info(self):
        (opts, args) = getopt.getopt(sys.argv[1:], 'p:', ['port='])
        try:
            if len(opts) != 1:
                raise getopt.GetoptError

            for (op, arg) in opts:
                if op == '-p' or op == '--port':
                    self.port = int(arg)
                else:
                    raise getopt.GetoptError

            if self.port is None:
                raise getopt.GetoptError

        except getopt.GetoptError:
            v.show_alert("Usage: server/app.py -p <port>")
            sys.exit(0)

    def interruption_handler(self, s, f):
        v.show_basic_message("Closing server...")
        self.server_serv.socket.close()
        sys.exit(0)

    def main(self):
        signal.signal(signal.SIGINT, self.interruption_handler)

        self.load_connection_info()
        v.show_info(f'\n --- "SUMAMOS" HELP CHAT SERVER --- \n\n Server running @ {self.host}:{self.port}')

        self.server_serv.socket.bind((self.host, self.port))
        self.server_serv.socket.listen()

        while True:
            c_socket, addr = self.server_serv.socket.accept()
            client_proc = multiprocessing.Process(target=self.server_serv.accept_connection, args=(c_socket, addr))
            client_proc.daemon = True
            client_proc.start()
