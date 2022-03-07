import multiprocessing


class PipeService:

    def __init__(self):
        self.client_pair, self.operator_pair = multiprocessing.Pipe(True)

    def send_msg_to_operator(self, msg: str):
        self.client_pair.send(msg)

    def send_msg_to_client(self, msg: str):
        self.operator_pair.send(msg)

    def get_msg_from_operator(self):
        return self.client_pair.recv()

    def get_msg_from_client(self):
        return self.operator_pair.recv()
