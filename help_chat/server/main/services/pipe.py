import multiprocessing


class PipeService:

    def __init__(self):
        # Instantiate a pipe and store its pairs for a bidirectional communication
        self.client_pair, self.operator_pair = multiprocessing.Pipe(duplex=True)

    def send_msg_to_operator(self, msg: str):
        self.client_pair.send(msg)  # CLIENT METHOD: sends a message to the operator

    def send_msg_to_client(self, msg: str):
        self.operator_pair.send(msg)  # OPERATOR METHOD: sends a message to the client

    def get_msg_from_operator(self):
        return self.client_pair.recv()  # CLIENT METHOD: receive a message from the operator

    def get_msg_from_client(self):
        return self.operator_pair.recv()  # OPERATOR METHOD: receive a message from the client
