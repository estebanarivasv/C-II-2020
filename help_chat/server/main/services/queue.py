import socket
import multiprocessing

from main.views import ConsoleView

v = ConsoleView()


class QueueService:

    # FIFO
    def __init__(self):
        self.queue = multiprocessing.Queue()

    def insert_sock_to_queue(self, sock: socket.socket):
        self.queue.put(sock)

    def get_sock_from_queue(self):
        return self.queue.get()

    def get_queue_size(self):
        return self.queue.qsize()
