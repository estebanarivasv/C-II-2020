import signal
import socket
import sys

from main.services.chat import ChatService
from main.views import ConsoleView

v = ConsoleView()


class ClientService:

    def __init__(self):
        """
        When instanced, a socket that is going to connect with the server is created.
        """
        try:
            # Socket that communicates with the server
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error as e:
            v.show_warning(f"Socket error: {e}")
            sys.exit(0)

    def close_server_socket(self):
        self.server_socket.close()

    def interruption_handler(self, s, f):
        # CTRL + C --- Signal handler
        self.close_server_socket()
        sys.exit(0)

    def connect_to_server(self, host, port):
        try:
            self.server_socket.connect((host, port))
        except Exception as e:
            v.show_warning(f"\n\nCONNECTION ERROR: {e}\n")
            sys.exit(0)

    def send_conn_info(self, department):
        """
        Sends a list with the type of user that tries to connect (client),
        and the department to which the user is trying to connect to.
        """
        chat_service = ChatService(self.server_socket)
        try:
            # Send client data to establish communication with the server
            chat_service.send_message(str(["client", department]))
        except Exception as e:
            v.show_warning(f"Connection error: {e}\n")

    def main(self, host, port, department):
        """
        Helps with server connection and chat between clients and operators
        """

        server_chat = ChatService(self.server_socket)
        signal.signal(signal.SIGINT, self.interruption_handler)

        v.show_info(v.return_welcome_msg(host, port))  # Print welcome message

        self.connect_to_server(host, port)  # Establish connection
        self.send_conn_info(department)  # Send info to server

        v.show_alert(
            f'\n\nYou asked to talk with {str(department).upper()} SUPPORT.'
            f'\nPlease wait...\n'
        )

        v.show_response(server_chat.receive_message())  # Awaiting an operator to connect
        server_chat.start_conversation()

        self.close_server_socket()
        sys.exit(0)
