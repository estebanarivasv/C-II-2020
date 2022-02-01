import socket
import sys
import multiprocessing

from main.views import ConsoleView
from main.models import ClientModel
from main.services.chat import ChatService

v = ConsoleView()


class ServerService:

    def __init__(self):
        self.technical_support_queue = multiprocessing.Queue()
        self.administrative_support_queue = multiprocessing.Queue()
        self.sales_support_queue = multiprocessing.Queue()
        self.chat_service = ChatService()

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            v.show_warning(f"Socket error: {e}\n")
            sys.exit(0)

    @staticmethod
    def get_from_client(client_sock: socket.socket):
        return client_sock.recv(1024).decode("utf-8")

    @staticmethod
    def send_to_client(client_sock: socket.socket, msg: str):
        return client_sock.send(msg.encode("utf-8"))

    def handle_connection(self, client_sock, client_addr):
        # Get role and department from client
        chat_info = eval(self.get_from_client(client_sock))
        client = ClientModel(client_addr[0], client_addr[1], chat_info[0], chat_info[1], client_sock)

        v.show_alert(f"\nConnection received form {client.host}:{client.port}.")
        # TODO: Delete
        print("\n", client.port, client.host, client.department, client.socket, client.role)

        # Put the client in a queue
        if client.role == 'client':
            if client.department == 'technical':
                self.technical_support_queue.put(client.socket)
            elif client.department == 'administrative':
                self.administrative_support_queue.put(client.socket)
            elif client.department == 'sales':
                self.sales_support_queue.put(client.socket)
            else:
                self.send_to_client(client.socket, "The specified department is incorrect")
                client.socket.close()
                sys.exit(0)

        # Insert an operator in a chat.
        elif client.role == 'operator':
            if client.department == 'technical':
                while True:
                    client_socket = self.technical_support_queue.get()
                    if client_socket:
                        chat_proc = multiprocessing.Process(
                            target=self.chat_service.start_chat,
                            args=(client.socket, client_socket)
                        )
                        chat_proc.daemon = True
                        chat_proc.start()
            if client.department == 'administrative':
                while True:
                    client_socket = self.administrative_support_queue.get()
                    if client_socket:
                        chat_proc = multiprocessing.Process(
                            target=self.chat_service.start_chat,
                            args=(client.socket, client_socket)
                        )
                        chat_proc.daemon = True
                        chat_proc.start()
            if client.department == 'sales':
                while True:
                    client_socket = self.sales_support_queue.get()
                    if client_socket:
                        chat_proc = multiprocessing.Process(
                            target=self.chat_service.start_chat,
                            args=(client.socket, client_socket)
                        )
                        chat_proc.daemon = True
                        chat_proc.start()
            else:
                self.send_to_client(client.socket, "The specified department is incorrect")
                client.socket.close()
                sys.exit(0)
        else:
            self.send_to_client(client.socket, "The specified role is incorrect")
            client.socket.close()
            sys.exit(0)
