import socket

from main.views import ConsoleView

v = ConsoleView()


class ChatService:

    def __init__(self, new_socket: socket.socket):
        self.sock = new_socket

    def receive_message(self):
        return self.sock.recv(1024).decode("utf-8")

    def send_message(self, msg: str):
        self.sock.send(msg.encode("utf-8"))

    def start_conversation(self):
        msg = ""
        while msg != "/exit":
            from_msg = self.receive_message()

            if from_msg == "/exit":
                break

            if from_msg:
                v.show_response(from_msg)
                msg = from_msg

            to_msg = v.ask_user_input()
            if to_msg:
                self.send_message(to_msg)
                msg = to_msg
