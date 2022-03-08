import socket
import sys
import threading
import time

from main.config import session
from main.services.chat import ChatService
from main.services.pipe import PipeService
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
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Make port reusable
        except socket.error as e:
            v.show_warning(f"Socket error: {e}\n")
            sys.exit(0)

    def get_client_data(self, client_sock: socket.socket):
        """
        Stores the data returns it as a list [user_type, department]
        """
        chat = ChatService(client_sock)
        return eval(chat.receive_message())  # Parsing role and department from str to list

    def authenticate_operator(self, client_sock: socket.socket):
        """
        Authenticates the operator:
        1- Asks for login info: username, password
        2- Checks for it existence in the db
        3- Retrieves a status message
        """
        chat = ChatService(client_sock)

        chat.send_message("\n<SERVER> Username: ")
        user_name = chat.receive_message()

        chat.send_message("\n<SERVER> Password: ")
        password = chat.receive_message()

        try:
            operator_from_db = session.query(OperatorModel).filter_by(username=user_name).first()

            if operator_from_db is not None and operator_from_db.password == password:
                chat.send_message("<SERVER> OK")
            else:
                chat.send_message("<SERVER> Wrong credentials")
        except Exception as e:
            v.show_warning(f"\nQUERY ERROR: {e}")
            chat.send_message("<SERVER> Internal error")

    def put_pipe_serv_in_queue(self, pipe: PipeService, department):
        """
        Adds PipeService instance to the FIFO queue in order to be consumed.
        """
        if department == 'technical':
            self.technical_service.insert_pipe_serv_to_queue(pipe)
        elif department == 'administrative':
            self.administrative_service.insert_pipe_serv_to_queue(pipe)
        elif department == 'sales':
            self.sales_service.insert_pipe_serv_to_queue(pipe)

    def get_pipe_serv_from_queue(self, department) -> PipeService:
        """
        Consumes the FIFO queue to get a PipeService instance.
        """
        if department == 'technical':
            return self.technical_service.get_pipe_serv_from_queue()
        elif department == 'administrative':
            return self.administrative_service.get_pipe_serv_from_queue()
        elif department == 'sales':
            return self.sales_service.get_pipe_serv_from_queue()

    def get_queue_size(self, department):
        """
        Consumes the pipe service from the queue.
        """
        if department == 'technical':
            return self.technical_service.get_num_elements_in_queue()
        elif department == 'administrative':
            return self.administrative_service.get_num_elements_in_queue()
        elif department == 'sales':
            return self.sales_service.get_num_elements_in_queue()

    def guide_operator(self, operator_sock: socket.socket, operator_department):
        """
        Method that handles operator protocol: authentication and looped chat with clients
        """
        chat = ChatService(operator_sock)

        self.authenticate_operator(operator_sock)  # Authenticate user

        while True:
            # Tests if queue has elements and sends it to the operator. If not, tries for every 15 seconds.
            if self.get_queue_size(operator_department) > 0:

                # Get pipe service from the queue to interact with client
                pipe_service = self.get_pipe_serv_from_queue(operator_department)

                chat.send_message("Connecting to a new client...")

                # Receive and send data to client socket through pipe
                while True:
                    # Get message from operator and send it to client in pipe
                    op_msg = chat.receive_message()
                    if op_msg == "/exit":
                        pipe_service.send_msg_to_client("/exit")
                        break
                    if op_msg != "":
                        pipe_service.send_msg_to_client(op_msg)

                    cl_msg = pipe_service.get_msg_from_client()
                    if cl_msg == "/exit":
                        chat.send_message("/exit")
                        break
                    elif cl_msg != "":
                        # Send message from client and send it to operator in socket
                        chat.send_message("<CLIENT> " + cl_msg)
            time.sleep(15)

    def guide_client(self, client_sock: socket.socket, client_department):
        """
        Method that handles client protocol: chat with operators
        """
        chat = ChatService(client_sock)

        # Create a pipe and send it to the queue
        pipe_service = PipeService()
        self.put_pipe_serv_in_queue(pipe_service, client_department)

        chat.send_message("Please wait for the operator to connect...\n")

        # Receive and send data to operator socket through pipe
        while True:
            op_msg = pipe_service.get_msg_from_operator()
            if op_msg == "/exit":
                chat.send_message("/exit")
                break
            if op_msg:
                # Send message from operator and send it to client socket
                chat.send_message("<OPERATOR> " + op_msg)

            # Get message from client and send it to operator in pipe
            cl_msg = chat.receive_message()
            if cl_msg == "/exit":
                pipe_service.send_msg_to_operator("/exit")
                break
            if cl_msg:
                pipe_service.send_msg_to_operator(cl_msg)

    def handle_connection(self, client_sock: socket.socket, client_addr):
        """
        Store the values form parameters, check type of user and "guide" them.
        """

        # Create entity instance
        client_data = self.get_client_data(client_sock)
        client_department = client_data[1]
        client_role = client_data[0]

        v.show_alert(f"\nNew connection received - {client_addr[0]}:{client_addr[1]}.\n")

        if client_role == 'client':
            self.guide_client(client_sock, client_department)

        elif client_role == 'operator':
            self.guide_operator(client_sock, client_department)

    def main(self, server_host, server_port):
        """
        Helps with handle the server-side chat between clients and operators
        """

        # Print the server address: ip, port
        if server_host == "":
            v.show_info(v.return_welcome_msg('0.0.0.0', server_port))
        else:
            v.show_info(v.return_welcome_msg(server_host, server_port))

        # Socket configuration
        self.server_socket.bind((server_host, server_port))  # Create socket
        self.server_socket.listen()  # Start to listen for clients

        while True:
            c_socket, addr = self.server_socket.accept()  # Accept connections
            client_proc = threading.Thread(
                target=self.handle_connection,
                args=(c_socket, addr)
            )
            client_proc.daemon = True  # When a process exits, attempts to terminate all of its daemonic child processes
            client_proc.start()
