import getopt
import signal
import socket
import sys
from main.views import ConsoleView

v = ConsoleView()


class ClientController:
    def __init__(self):
        self.server_host = None
        self.server_port = None
        self.user_department = None
        self.user_role = None
        self.socket = None

    def check_not_null(self):
        for i in [self.server_host, self.server_port, self.user_department, self.user_role]:
            if i is None:
                return False
            else:
                return True

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

            if not self.check_not_null():
                raise Exception

        except getopt.GetoptError or TypeError:
            v.show_alert("\nUsage: client/app.py -h <host> -p <port> -d <department> -r <role>\n")
            sys.exit(0)

    def create_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            v.show_warning(f"Socket error: {e}")
            sys.exit()

    def interruption_handler(self):
        v.show_basic_message("Closing connection...")
        self.socket.close()

    def handle_inputs_outputs(self):
        # IF THE USER SENDS AN interrupt signal
        signal.signal(signal.SIGINT, self.interruption_handler)

        while True:
            msg_from_server = self.socket.recv(1024).decode('utf-8')
            v.show_server_response(f"\n\n <-- {msg_from_server}")

            if msg_from_server == "\n" or "":
                break


            v.show_user_input("\n\n --> ")
            msg_to_server = input().encode('utf-8')

            self.socket.send(msg_to_server)


            # todo: handle logging in order to skip "department" and "role"
