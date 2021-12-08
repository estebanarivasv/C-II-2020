import getopt
import multiprocessing
import signal
import socket
import sys
from main.views.console import ConsoleView

v = ConsoleView()


class ServerController:

    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = None
        self.socket = None

    def check_not_null(self):
        if self.port is None:
            return False
        else:
            return True

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

            if not self.check_not_null():
                raise getopt.GetoptError

        except getopt.GetoptError:
            v.show_alert("Usage: server/app.py -p <port>")
            sys.exit(0)

    def create_socket(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
        except socket.error as e:
            v.show_warning(f"Socket error: {e}")
            sys.exit()

    def interruption_handler(self):
        v.show_basic_message("Closing server...")
        self.socket.close()

    def handle_inputs_outputs(self, client_sock, address):
        signal.signal(signal.SIGINT, self.interruption_handler)

        print(f"\nReceived connection form {address[0]}:{address[1]}.")

        welcome_msg = '\n\n --- "SUMAMOS" HELP CHAT SERVER --- \n\n Welcome!'
        client_sock.send(welcome_msg.encode("utf-8"))

        while True:
            msg_from_client = client_sock.recv(1024).decode("utf-8")

            if msg_from_client == "\n" or "":
                break

            v.show_client_response(f" <-- {msg_from_client}")

            client_sock.send("next".encode("utf-8"))

        print("Closing server...")
        self.socket.close()

    def receive_connections(self):
        self.socket.listen()
        while True:
            c_socket, addr = self.socket.accept()
            client_proc = multiprocessing.Process(target=self.handle_inputs_outputs, args=(c_socket, addr))
            client_proc.start()
