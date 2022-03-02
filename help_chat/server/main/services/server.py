import socket
import sys
import multiprocessing
import time

from main.config import session
from main.services.chat import ChatService
from main.services.queue import QueueService
from main.views import ConsoleView
from main.models import OperatorModel

v = ConsoleView()


class ServerService:

    def __init__(self):
        self.technical_service = QueueService()
        self.administrative_service = QueueService()
        self.sales_service = QueueService()
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            v.show_warning(f"Socket error: {e}\n")
            sys.exit(0)

    def get_client_data(self, client_sock: socket.socket):
        chat = ChatService(client_sock)

        # Parsing role and department from str to list
        return eval(chat.receive_message())

    def authenticate_operator(self, client_sock: socket.socket):
        chat = ChatService(client_sock)

        chat.send_message("\nUsername: ")
        user_name = chat.receive_message()

        chat.send_message("\nPassword: ")
        password = chat.receive_message()

        try:
            operator_from_db = session.query(OperatorModel).filter_by(username=user_name).first()

            if operator_from_db is not None and operator_from_db.password == password:
                chat.send_message("OK")
            else:
                chat.send_message("WRONG CREDENTIALS")
        except Exception as e:
            v.show_warning(f"\nQUERY ERROR: {e}")
            chat.send_message("INTERNAL ERROR")

    def put_client_in_queue(self, ip, port, department):
        if department == 'technical':
            self.technical_service.insert_sock_addr_to_queue(str([ip, port]))
        elif department == 'administrative':
            self.administrative_service.insert_sock_addr_to_queue(str([ip, port]))
        elif department == 'sales':
            self.sales_service.insert_sock_addr_to_queue(str([ip, port]))

    def get_client_from_queue(self, department):
        if department == 'technical':
            return self.technical_service.get_sock_addr_from_queue()
        elif department == 'administrative':
            return self.administrative_service.get_sock_addr_from_queue()
        elif department == 'sales':
            return self.sales_service.get_sock_addr_from_queue()
        else:
            return None

    def get_queue_size(self, department):
        if department == 'technical':
            return self.technical_service.get_queue_size()
        elif department == 'administrative':
            return self.administrative_service.get_queue_size()
        elif department == 'sales':
            return self.sales_service.get_queue_size()

    def guide_operator(self, operator_sock: socket.socket, operator_department):
        self.authenticate_operator(operator_sock)

        while True:

            if self.get_queue_size(operator_department) > 0:
                # print(f"\n\n{operator_department} queue size", self.get_queue_size(operator_department))
                client_addr = self.get_client_from_queue(operator_department)

                operator_chat = ChatService(operator_sock)
                operator_chat.send_message(client_addr)

            time.sleep(15)

    def guide_client(self, ip, port, department):
        self.put_client_in_queue(ip, port, department)

    def handle_connection(self, client_sock: socket.socket, client_addr):

        # Create entity instance
        client_data = self.get_client_data(client_sock)
        client_department = client_data[1]
        client_role = client_data[0]

        v.show_alert(f"\nNew connection received - {client_addr[0]}:{client_addr[1]}.\n")

        if client_role == 'client':
            self.guide_client(client_addr[0], client_addr[1], client_department)

        elif client_role == 'operator':
            self.guide_operator(client_sock, client_department)

        v.show_server_log(f"\nSaving data in queue and closing connection with"
                          f" socket {client_addr[0]}:{client_addr[1]}.\n")
        client_sock.close()

    def main(self, server_host, server_port):
        # Make port reusable
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        v.show_info(v.return_welcome_msg(server_host, server_port))

        # Socket configuration
        self.server_socket.bind((server_host, server_port))  # Create socket
        self.server_socket.listen()  # Start to listen for clients

        while True:
            c_socket, addr = self.server_socket.accept()
            client_proc = multiprocessing.Process(
                target=self.handle_connection,
                args=(c_socket, addr)
            )
            client_proc.daemon = True
            client_proc.start()
