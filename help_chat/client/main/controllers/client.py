import getopt
import sys

from main.views import ConsoleView
from main.services import ClientService
from main.services import OperatorService

v = ConsoleView()


class ClientController:
    def __init__(self):
        self.server_host = None
        self.server_port = None
        self.user_department = None
        self.user_role = None

    def load_connection_info(self):
        (opts, args) = getopt.getopt(sys.argv[1:], 'h:p:d:r:', ['host=', 'port=', 'department=', 'role='])
        try:
            if len(opts) != 4:
                raise getopt.GetoptError(v.return_usage())

            for (op, arg) in opts:
                if op == '-h' or op == '--host':
                    self.server_host = arg
                elif op == '-p' or op == '--port':
                    self.server_port = int(arg)
                elif op == '-d' or op == '--department':
                    self.user_department = arg
                elif op == '-r' or op == '--role':
                    self.user_role = arg

            for i in [self.server_host, self.server_port, self.user_department, self.user_role]:
                if i is None:
                    raise getopt.GetoptError(v.return_usage())

        except getopt.GetoptError or TypeError:
            v.show_alert(v.return_usage())
            sys.exit(0)

    def main(self):
        # Fetch data from parameters
        self.load_connection_info()

        # Set application mode: 'client' or 'operator'
        if self.user_role == "client":
            client_service = ClientService()
            client_service.main(self.server_host,
                                self.server_port,
                                self.user_department)

        # Authenticate and get client data from Queue
        elif self.user_role == "operator":
            operator_service = OperatorService()
            operator_service.main(self.server_host,
                                  self.server_port,
                                  self.user_department)
        else:
            v.show_alert("Wrong input in user role.")
            sys.exit(0)
