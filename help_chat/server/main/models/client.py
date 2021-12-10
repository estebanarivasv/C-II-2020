from socket import socket as sock


class ClientModel:

    def __init__(self, host, port, department, role, socket: sock):
        self.host = host
        self.port = port
        self.department = department
        self.role = role
        self.socket = socket
