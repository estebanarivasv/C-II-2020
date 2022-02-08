import socket
import sys
import multiprocessing

from main.services.chat import ChatService
from main.services.chat_room import ChatRoomService
from main.services.queue import QueueService
from main.views import ConsoleView
from main.models import ClientModel

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

    def handle_connection(self, client_sock, client_addr):

        chat_service = ChatService(client_sock)

        # Get role and department from client
        chat_info = eval(chat_service.receive_message())  # Parsing from str to list

        # Setting client data
        client = ClientModel(
            host=client_addr[0],
            port=client_addr[1],
            department=chat_info[1],
            role=chat_info[0],
            socket=client_sock
        )

        v.show_alert(f"\n\nNew connection received - {client_addr[0]}:{client_addr[1]}.")

        # TODO: Delete
        print("\nSOCKET VALUE: ", client_sock)

        if client.role == 'client':
            chat_service.send_message(
                f'You asked to talk with {str(client.department).upper()} SUPPORT.'
                f'\nPlease wait...\n'
            )

            if client.department == 'technical':
                self.technical_service.insert_client_to_queue(client)
            elif client.department == 'administrative':
                self.administrative_service.insert_client_to_queue(client)
            elif client.department == 'sales':
                self.sales_service.insert_client_to_queue(client)
            else:
                self.server_socket.close()

        elif client.role == 'operator':
            # TODO: self.authenticate_operator()
            while True:
                operator = client
                if client.department == 'technical':
                    client = self.technical_service.get_client_from_queue()
                elif client.department == 'administrative':
                    client = self.administrative_service.get_client_from_queue()
                elif client.department == 'sales':
                    client = self.sales_service.get_client_from_queue()
                else:
                    self.server_socket.close()

                chat_room_service = ChatRoomService(client, operator)
                chat_room_service.start_chat()

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
