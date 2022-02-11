import signal
import socket
import sys

from main.services.chat import ChatService
from main.views import ConsoleView

v = ConsoleView()


class ClientService:
    def __init__(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            v.show_warning(f"Socket error: {e}")
            sys.exit(0)

    def close_server_socket(self):
        self.server_socket.close()

    def interruption_handler(self, s, f):
        self.close_server_socket()
        sys.exit(0)

    def connect_to_server(self, host, port):
        try:
            self.server_socket.connect((host, port))
        except Exception as e:
            v.show_warning(f"\n\nCONNECTION ERROR: {e}\n")
            sys.exit(0)

    def send_conn_info(self, department):

        chat_service = ChatService(self.server_socket)
        try:
            # Send client data to establish communication with the server
            chat_service.send_message(str(["client", department]))
            msg = chat_service.receive_message()
            v.show_server_response(msg)
        except Exception as e:
            v.show_warning(f"Connection error: {e}\n")

    def main(self, host, port, department):
        # CTRL + C - Stops client
        signal.signal(signal.SIGINT, self.interruption_handler)
        chat_service = ChatService(self.server_socket)

        v.show_info(v.return_welcome_msg(host, port))

        self.connect_to_server(host, port)
        self.send_conn_info(department)

        chat_service.start_conversation()

        self.close_server_socket()
        sys.exit(0)
