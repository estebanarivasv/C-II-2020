import signal

from main.views import ConsoleView
from main.controllers import ServerController

v = ConsoleView()

if __name__ == '__main__':
    try:
        server = ServerController()
        server.load_connection_info()
        server.create_socket()
        v.show_basic_message('\n --- "SUMAMOS" HELP CHAT SERVER --- \n')
        v.show_basic_message(f"Server running @ {server.host}:{server.port}")
        # IF THE USER SENDS AN interrupt signal
        server.receive_connections()

    except ConnectionResetError:
        v.show_warning("Connection reset by peer")
