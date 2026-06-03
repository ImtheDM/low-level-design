from abc import ABC, abstractmethod

class Logger(ABC):

    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def log(self, log_name, message):
        if(self.next_handler != None):
            self.next_handler.log(log_name, message)