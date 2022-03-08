from multiprocessing import Manager

from main.services.pipe import PipeService
from main.views import ConsoleView

v = ConsoleView()


class QueueService:

    # FIFO
    def __init__(self):
        self.queue = Manager().list()  # Holds the list and allows other processes to manipulate it using a proxy

    def insert_pipe_serv_to_queue(self, pipe: PipeService):
        self.queue.append(pipe)  # Add socket object to the end

    def get_pipe_serv_from_queue(self) -> PipeService:
        return self.queue.pop(0)  # Return socket object from the beginning

    def get_num_elements_in_queue(self):
        return len(self.queue)  # Get number of elements in the queue
