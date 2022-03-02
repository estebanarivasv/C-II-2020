import signal
import socket
import sys

from main.services.chat import ChatService
from main.views import ConsoleView

v = ConsoleView()


class OperatorService:

    def __init__(self):
        try:
            # Socket that connects to the client
            self.operator_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # This socket talks with the server
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            v.show_warning(f"Socket error: {e}")
            sys.exit(0)

    def close_sockets(self):
        self.operator_socket.close()
        self.server_socket.close()

    def interruption_handler(self, s, f):
        self.close_sockets()
        sys.exit(0)

    def connect_to_server(self, host, port):
        try:
            self.server_socket.connect((host, port))
        except Exception as e:
            v.show_warning(f"\n\nCONNECTION ERROR: {e}\n")
            sys.exit(0)

    def connect_to_client(self, host, port):
        try:
            v.show_info(f"\nAttempting to connect to {host}:{port}\n")
            self.operator_socket.connect((host, port))
            return self.operator_socket.getsockname()
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

        # Send username and password to server
        for i in range(2):
            v.show_response(chat.receive_message())
            msg = v.ask_user_input()
            chat.send_message(msg)

        status = chat.receive_message()
        v.show_response(status + "\n")
        if status == "OK":
            return True
        else:
            return False

    def main(self, host, port, department):
        # Signal TERM handler --- CTRL + C - Stops client
        signal.signal(signal.SIGINT, self.interruption_handler)

        server_chat = ChatService(self.server_socket)

        # Print welcome message
        v.show_info(v.return_welcome_msg(host, port))

        self.connect_to_server(host, port)

        self.send_conn_info(department)

        if self.is_authenticated() is True:
            # This loop iterates to get a new customer in the queue
            while True:
                client_addr = eval(server_chat.receive_message())

                from_address = self.connect_to_client(client_addr[0], client_addr[1])
                v.show_info(f'\nActual connection: {from_address[0]}:{from_address[1]}')

                operator_chat = ChatService(self.operator_socket)
                operator_chat.send_message(f"\nYou're now connected with an operator")

                operator_chat.start_conversation()

        self.close_sockets()
        sys.exit(0)
