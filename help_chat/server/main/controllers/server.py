import getopt
import multiprocessing
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
        self.server_serv = ServerService()

    def load_connection_info(self):
        (opts, args) = getopt.getopt(sys.argv[1:], 'p:', ['port='])
        try:
            if len(opts) != 1:
                raise getopt.GetoptError("Usage: server/app.py -p <port>")
            for (op, arg) in opts:
                if op == '-p' or op == '--port':
                    self.port = int(arg)
        except getopt.GetoptError:
            v.show_alert("Usage: server/app.py -p <port>")
            sys.exit(0)

    def interruption_handler(self, s, f):
        v.show_basic_message("\nClosing server...")
        self.server_serv.socket.close()
        sys.exit(0)

    def main(self):
        # CTRL + C - Stops server
        signal.signal(signal.SIGINT, self.interruption_handler)

        # Database configuration - SQL Alchemy
        Session = sessionmaker(bind=engine)
        session = Session()

        # Importing models
        from main.models import OperatorModel
        
        Base.metadata.create_all(bind=engine)

        self.load_connection_info()
        v.show_info(f'\n --- "SUMAMOS" HELP CHAT SERVER --- \n\n'
                    f' Server running @ {self.host}:{self.port}')

        self.server_serv.socket.bind((self.host, self.port))
        self.server_serv.socket.listen()

        while True:
            c_socket, addr = self.server_serv.socket.accept()
            client_proc = multiprocessing.Process(
                target=self.server_serv.handle_connection,
                args=(c_socket, addr))
            client_proc.daemon = True
            client_proc.start()
