import signal
import socket
import sys

from main.services.chat import ChatService
from main.views import ConsoleView

v = ConsoleView()


class ClientService:
    def __init__(self):
        self.client_host = socket.gethostbyname(socket.gethostname())
        self.client_port = 8090
        try:
            self.to_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            v.show_warning(f"Socket error: {e}")
            sys.exit(0)

    def close_server_socket(self):
        self.to_server_socket.close()

    def interruption_handler(self, s, f):
        self.close_server_socket()
        sys.exit(0)

    def establish_connection(self, department):

        chat_service = ChatService(self.to_server_socket)

        try:
            # Send client data to establish communication with the server
            chat_service.send_message(str(["client", department]))

            v.show_server_response(chat_service.receive_message())

        except ConnectionRefusedError as e:
            v.show_warning(f"Connection error: {e}\n")

    def main(self, host, port, department):
        # CTRL + C - Stops client
        signal.signal(signal.SIGINT, self.interruption_handler)

        v.show_info(v.return_welcome_msg(host, port))

        try:
            self.to_server_socket.connect((host, port))
            self.establish_connection(department)
        except Exception as e:
            v.show_warning(f"\n\nCONNECTION ERROR: {e}\n\n")
            sys.exit(0)

        chat_service = ChatService(self.to_server_socket)
        chat_service.start_conversation()
        """
        # Receive messages up until the server establishes connection with operator
        while True:
            msg = chat_service.receive_message()
            if msg == "Redirecting with operator...":
                v.show_server_response(msg)
                chat_service.start_conversation()
                break
            v.show_server_response(msg)
        """
        self.close_server_socket()
        sys.exit(0)
