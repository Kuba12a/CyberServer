from Logic.Commands.Commands import Command
from Utils.Singleton import Singleton
import queue


class CommandQueue(metaclass=Singleton):
    def __init__(self):
        self.queue = queue.Queue()

    def insert(self, item: Command):
        self.queue.put(item)

    def get(self) -> Command:
        if not self.queue.empty():
            return self.queue.get()
        return None
