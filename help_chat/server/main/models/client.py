from socket import socket as sock


class ClientModel:

    def __init__(self, host: str, port: int, department: str, role: str, socket: sock):
        self.host = host
        self.port = port
        self.department = department
        self.role = role
        self.socket = socket
