from main.views import ConsoleView
from main.controllers import ServerController

v = ConsoleView()

if __name__ == '__main__':
    server = ServerController()
    server.main()
