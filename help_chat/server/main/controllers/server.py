import getopt
import signal
import socket
import sys

from main.views import ConsoleView
from main.services import ServerService
from main.config import Base, engine

v = ConsoleView()


class ServerController:

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = None
        self.server_service = ServerService()

    def load_parameters(self):
        (opts, args) = getopt.getopt(sys.argv[1:], 'p:', ['port='])
        try:
            if len(opts) != 1:
                raise getopt.GetoptError(v.return_usage())
            for (op, arg) in opts:
                if op == '-p' or op == '--port':
                    self.port = int(arg)
        except getopt.GetoptError:
            v.show_alert(v.return_usage())
            sys.exit(0)

    def interruption_handler(self, s, f):
        v.show_basic_message("\nClosing server...\n")
        self.server_service.server_socket.close()
        sys.exit(0)

    def main(self):
        self.load_parameters()     # Receive parameters' values

        # CTRL + C - Stops server
        signal.signal(signal.SIGINT, self.interruption_handler)

        # Database configuration - SQL Alchemy
        from main.models import OperatorModel       # Importing models
        Base.metadata.create_all(bind=engine)
        self.server_service.main(self.host, self.port)
