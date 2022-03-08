import signal
import socket
import sys

from main.services.chat import ChatService
from main.views import ConsoleView

v = ConsoleView()


class OperatorService:

    def __init__(self):
        """
        When instanced, a socket that is going to connect with the server is created.
        """
        try:
            # Socket that communicates with the server
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            v.show_warning(f"Socket error: {e}")
            sys.exit(0)

    def close_sockets(self):
        self.server_socket.close()

    def interruption_handler(self, s, f):
        # CTRL + C --- Signal handler
        self.close_sockets()
        sys.exit(0)

    def connect_to_server(self, host, port):
        try:
            self.server_socket.connect((host, port))
        except Exception as e:
            v.show_warning(f"\n\nCONNECTION ERROR: {e}\n")
            sys.exit(0)

    def send_conn_info(self, department):
        """
        Sends a list with the type of user that tries to connect (operator),
        and the department to which the user is trying to connect to.
        """
        chat_service = ChatService(self.server_socket)
        try:
            # Send client data to establish communication with the server
            chat_service.send_message(str(["operator", department]))
        except Exception as e:
            v.show_warning(f"Connection error: {e}\n")

    def is_authenticated(self):
        """
        Checks if the user is able to authenticate
        once they deliver the login information
        """
        chat = ChatService(self.server_socket)

        # Send username and password to server
        for i in range(2):
            v.show_response(chat.receive_message())
            msg = v.ask_user_input()
            chat.send_message(msg)

        status = chat.receive_message()
        v.show_response(status + "\n")
        if status == "<SERVER> OK":
            return True
        else:
            return False

    def main(self, host, port, department):
        """
        Helps with server connection and chat between clients and operators
        """

        server_chat = ChatService(self.server_socket)
        signal.signal(signal.SIGINT, self.interruption_handler)

        v.show_info(v.return_welcome_msg(host, port))  # Print welcome message

        self.connect_to_server(host, port)  # Establish connection
        self.send_conn_info(department)  # Send info to server

        if self.is_authenticated() is True:
            # This loop iterates to get a new customer in the queue
            while True:
                server_chat.start_conversation()
                v.show_alert("\nChat ended."
                             "\nIn 15 seconds, the system is going to check and try to fetch a client "
                             "awaiting to be assisted in the queue...")
        self.close_sockets()
        sys.exit(0)
