import socket
import sys

from main.views import ConsoleView

v = ConsoleView()


class ClientService:

    def __init__(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            v.show_warning(f"Socket error: {e}")
            sys.exit(0)

    def send_to_server(self, msg):
        self.socket.send(msg.encode('utf-8'))

    def receive_from_server(self):
        return self.socket.recv(1024).decode('utf-8')

    def close_socket(self):
        self.socket.close()
