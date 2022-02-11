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
