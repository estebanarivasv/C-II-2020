import colored
from colored import stylize


class ConsoleView:

    @staticmethod
    def show_basic_message(msg):
        print(msg)

    @staticmethod
    def show_alert(msg):
        print(stylize(msg, colored.fg("orange_red_1")), end='')

    @staticmethod
    def show_warning(msg):
        print(stylize(msg, colored.fg("red")), end='')

    @staticmethod
    def ask_user_input():
        return input(stylize("\n\n<YOU> ", colored.fg("green")))

    @staticmethod
    def show_operator_response(msg, operator_name: str):
        print(stylize(f"\n\n<{operator_name.upper()}> " + msg, colored.fg("orange_4a")), end='')

    @staticmethod
    def show_server_response(msg):
        print(stylize('\n\n<SERVER> ' + msg, colored.fg("yellow")), end='')

    @staticmethod
    def show_info(msg):
        print(stylize(msg, colored.fg("cyan")), end='')

    @staticmethod
    def return_usage():
        return "\nUsage: client/app.py -h <server_host> -p <server_port> -d <department> -r <role>\n"

    @staticmethod
    def return_welcome_msg(server_host, server_port):
        return f"\n--- 'SUMAMOS' HELP CHAT SERVER --- \n" \
               f"\nConnecting to server --> {server_host}:{server_port}."
