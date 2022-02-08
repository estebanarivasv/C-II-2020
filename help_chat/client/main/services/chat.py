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
            msg = self.receive_message()
            print(self.sock)
            v.show_server_response(msg)

            v.show_user_input()
            self.send_message(input())
        self.sock.close()
