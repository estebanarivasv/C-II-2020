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
    def show_user_input():
        print(stylize("\n\n --> ", colored.fg("green")), end='')

    @staticmethod
    def show_server_response(msg):
        print(stylize('\n\n <--' + msg, colored.fg("yellow")), end='')

    @staticmethod
    def show_info(msg):
        print(stylize(msg, colored.fg("cyan")), end='')

