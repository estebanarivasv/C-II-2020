from socket import socket as sock


class ClientModel:

    def __init__(self, host: str, port: int, department: str, role: str, socket: sock):
        self.host = host
        self.port = port
        self.department = department
        self.role = role
        self.socket = socket

    def __repr__(self):
        return f"\n{str(self.port)} {self.host} {self.department} {str(self.socket)} {self.role}"
