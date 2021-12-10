import socket
import sys


class ChatService:

    @staticmethod
    def get_from_client(sock: socket.socket):
        if sock.recv(1024).decode("utf-8") == '/exit':
            sys.exit(0)
        return sock.recv(1024).decode("utf-8")

    @staticmethod
    def send_to_client(sock: socket.socket, msg: str):
        return sock.send(msg.encode("utf-8"))

    def start_chat(self, operator_sock: socket.socket, client_sock: socket.socket):
        while True:
            msg_from_operator = self.get_from_client(operator_sock)
            self.send_to_client(client_sock, msg_from_operator)
