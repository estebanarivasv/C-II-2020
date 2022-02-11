import socket

from main.models import ClientModel
from main.services.chat import ChatService
from main.views import ConsoleView

v = ConsoleView()


class ChatRoomService:

    def __init__(self, c_sock: socket.socket, o_sock: socket.socket):
        self.c_sock = c_sock
        self.o_sock = o_sock

    def start_chat(self):
        client_connection = ChatService(self.c_sock)
        operator_connection = ChatService(self.o_sock)

        print("\n\n\n\npor enviar start...")
        operator_connection.send_message("START")
        client_connection.send_message("START")

        from_operator = ""
        from_client = ""
        while from_operator != "/exit" or from_client != "/exit":
            from_operator = operator_connection.receive_message()
            if from_operator != "":
                client_connection.send_message(from_operator)
            from_client = client_connection.receive_message()
            if from_client != "":
                operator_connection.send_message(from_client)
        client_connection.sock.close()
