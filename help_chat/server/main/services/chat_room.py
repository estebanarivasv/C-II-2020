from main.models import ClientModel
from main.services.chat import ChatService
from main.views import ConsoleView

v = ConsoleView()


class ChatRoomService:

    def __init__(self, client: ClientModel, operator: ClientModel):
        self.client = client
        self.operator = operator

    def start_chat(self):
        client_connection = ChatService(self.client.socket)
        operator_connection = ChatService(self.operator.socket)

        operator_connection.send_message("START")

        msg = ""
        while msg != "/exit":
            msg = operator_connection.receive_message()
            client_connection.send_message(msg)

            msg = client_connection.receive_message()
            operator_connection.send_message(msg)
        client_connection.sock.close()
