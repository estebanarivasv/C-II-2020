from main.controllers import ClientController
from main.views import ConsoleView

v = ConsoleView()

if __name__ == '__main__':
    try:
        client = ClientController()
        client.load_connection_info()
        client.create_socket()
        client.socket.connect((client.server_host, client.server_port))
        client.handle_inputs_outputs()
    except ConnectionRefusedError:
        v.show_warning("The help chat server is not running")


