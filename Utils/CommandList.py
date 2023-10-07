from Logic.Commands.Commands import Command
from Utils.Singleton import Singleton


class CommandList(metaclass=Singleton):
    def __init__(self):
        self.list = []

    def insert(self, item: Command):
        self.list.append(item)

    def get_first_by_ip(self, ip_address) -> Command:
        command = next((c for c in self.list if c.ip_address == ip_address), None)
        if command:
            self.list.remove(command)
        return command
