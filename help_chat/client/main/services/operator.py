import signal
import socket
import sys

from main.services.chat import ChatService
from main.views import ConsoleView

v = ConsoleView()


class OperatorService:

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
            chat_service.send_message(str(["operator", department]))
        except Exception as e:
            v.show_warning(f"Connection error: {e}\n")

    def is_authenticated(self):
        chat = ChatService(self.server_socket)
        for i in range(2):
            v.show_server_response(chat.receive_message())
            msg = v.ask_user_input()
            chat.send_message(msg)
        status = chat.receive_message()
        v.show_server_response(status)
        if status == "OK":
            return True
        else:
            return False

    def main(self, host, port, department):
        # Signal TERM handler --- CTRL + C - Stops client
        signal.signal(signal.SIGINT, self.interruption_handler)
        chat_service = ChatService(self.server_socket)

        # Print welcome message
        v.show_info(v.return_welcome_msg(host, port))

        self.connect_to_server(host, port)
        self.send_conn_info(department)
        status = self.is_authenticated()

        if status is True:
            while True:
                chat_service = ChatService(self.server_socket)
                chat_service.start_conversation()

        self.close_server_socket()
        sys.exit(0)
