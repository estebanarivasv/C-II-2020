import socket
import multiprocessing

from main.models import ClientModel
from main.views import ConsoleView

v = ConsoleView()


class QueueService:

    # FIFO
    def __init__(self):
        self.queue = multiprocessing.Queue()

    def insert_client_to_queue(self, client: ClientModel):
        self.queue.put(client)

    def get_client_from_queue(self):
        return self.queue.get()

    def get_queue_size(self):
        return self.queue.qsize()

