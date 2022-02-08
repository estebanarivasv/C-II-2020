import getopt
import signal
import socket
import sys
from sqlalchemy.orm import sessionmaker

from main.views import ConsoleView
from main.services import ServerService
from main.config import Base, engine

v = ConsoleView()


class ServerController:

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = None
        self.server_service = ServerService()

    def load_connection_info(self):
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
        v.show_basic_message("\nClosing server...")
        self.server_service.server_socket.close()
        sys.exit(0)

    def main(self):
        # CTRL + C - Stops server
        signal.signal(signal.SIGINT, self.interruption_handler)

        # Database configuration - SQL Alchemy
        Session = sessionmaker(bind=engine)
        session = Session()
        from main.models import OperatorModel       # Importing models
        Base.metadata.create_all(bind=engine)

        self.load_connection_info()     # Receive parameters' values
        self.server_service.main(self.host, self.port)