import signal
import socket
import sys

from main.services.chat import ChatService
from main.views import ConsoleView

v = ConsoleView()


class ClientService:
    def __init__(self):
        try:
            # Socket that communicates with the server
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Socket that receives connections from operators.
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error as e:
            v.show_warning(f"Socket error: {e}")
            sys.exit(0)

    def close_client_socket(self):
        self.client_socket.close()

    def close_server_socket(self):
        self.server_socket.close()

    def interruption_handler(self, s, f):
        self.close_client_socket()
        sys.exit(0)

    def connect_to_server(self, host, port):
        try:
            self.server_socket.connect((host, port))
            return self.server_socket.getsockname()
        except Exception as e:
            v.show_warning(f"\n\nCONNECTION ERROR: {e}\n")
            sys.exit(0)

    def send_conn_info(self, department):

        chat_service = ChatService(self.server_socket)
        try:
            # Send client data to establish communication with the server
            chat_service.send_message(str(["client", department]))
        except Exception as e:
            v.show_warning(f"Connection error: {e}\n")

    def main(self, host, port, department):
        # CTRL + C - Stops client
        signal.signal(signal.SIGINT, self.interruption_handler)

        v.show_info(v.return_welcome_msg(host, port))

        from_address = self.connect_to_server(host, port)

        # Todo: Sends role as 'client' and department value
        self.send_conn_info(department)

        self.server_socket.close()
        self.close_server_socket()

        v.show_alert(
            f'\n\nYou asked to talk with {str(department).upper()} SUPPORT.'
            f'\nPlease wait...\n'
        )
        v.show_info(f'\nActual connection: {from_address[0]}:{from_address[1]}')

        # Socket that awaits for an operator to connect
        self.client_socket.bind((from_address[0], from_address[1]))  # Create socket
        self.client_socket.listen(1)  # Start to listen for operator

        v.show_alert(
            f'\n\nListening for connections...'
        )

        o_socket, addr = self.client_socket.accept()

        print("\nConectira suksesfuli", addr)

        chat_service = ChatService(o_socket)
        chat_service.start_conversation()

        self.close_client_socket()
        sys.exit(0)
