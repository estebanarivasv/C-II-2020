import getopt
import signal
import sys

from main.views import ConsoleView
from main.services import ClientService

v = ConsoleView()


class ClientController:
    def __init__(self):
        self.server_host = None
        self.server_port = None
        self.user_department = None
        self.user_role = None
        self.client_serv = ClientService()

    def load_connection_info(self):
        (opts, args) = getopt.getopt(sys.argv[1:], 'h:p:d:r:', ['host=', 'port=', 'department=', 'role='])
        try:
            if len(opts) != 4:
                raise getopt.GetoptError

            for (op, arg) in opts:
                if op == '-h' or op == '--host':
                    self.server_host = arg
                elif op == '-p' or op == '--port':
                    self.server_port = int(arg)
                elif op == '-d' or op == '--department':
                    self.user_department = arg
                elif op == '-r' or op == '--role':
                    self.user_role = arg
                else:
                    raise getopt.GetoptError

            for i in [self.server_host, self.server_port, self.user_department, self.user_role]:
                if i is None:
                    raise getopt.GetoptError
                else:
                    pass

        except getopt.GetoptError or TypeError:
            v.show_alert("\nUsage: client/app.py -h <host> -p <port> -d <department> -r <role>\n")
            sys.exit(0)

    def start_chat(self):
        try:
            # Send client config to establish communication
            chat_info = str([self.user_role, self.user_department])
            self.client_serv.send_to_server(chat_info)

            msg_from_server = None
            while msg_from_server != "/exit":
                msg_from_server = self.client_serv.receive_from_server()
                v.show_server_response(msg_from_server)

                v.show_user_input()
                msg_to_server = input()
                self.client_serv.send_to_server(msg_to_server)

        except ConnectionRefusedError as e:
            v.show_warning(f"Connection error: {e}\n")

    def interruption_handler(self, s, f):
        self.client_serv.close_socket()
        sys.exit(0)

    def main(self):
        signal.signal(signal.SIGINT, self.interruption_handler)

        self.load_connection_info()
        self.client_serv.socket.connect((self.server_host, self.server_port))

        v.show_info(f'\n --- "SUMAMOS" HELP CHAT SERVER --- \n\n'
                    f' Connecting to server --> {self.server_host}:{self.server_port}.\n'
                    f' You asked to talk to {str(self.user_department).upper()} SUPPORT.\n'
                    f' Please wait...\n')
        self.start_chat()
