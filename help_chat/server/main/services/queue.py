import socket
import multiprocessing

from main.views import ConsoleView

v = ConsoleView()


class QueueService:

    # FIFO
    def __init__(self):
        self.queue = multiprocessing.Queue()

    def insert_sock_addr_to_queue(self, addr: ()):
        self.queue.put(addr)

    def get_sock_addr_from_queue(self):
        return self.queue.get()

    def get_queue_size(self):
        return self.queue.qsize()
