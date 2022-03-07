from multiprocessing import Manager

from main.services.pipe import PipeService
from main.views import ConsoleView

v = ConsoleView()


class QueueService:

    # FIFO
    def __init__(self):
        self.queue = Manager().list()

    def insert_pipe_serv_to_queue(self, pipe: PipeService):
        # Add socket object to the end
        self.queue.append(pipe)

    def get_pipe_serv_from_queue(self) -> PipeService:
        # Return socket object from the beginning
        return self.queue.pop(0)

    def get_num_elements_in_queue(self):
        # Get number of elements in the queue
        return len(self.queue)
