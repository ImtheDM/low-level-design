from .base import Logger

class Info(Logger):

    def __init__(self, next_handler=None):
        super().__init__(next_handler)

    def log(self, log_name, message):
        if(log_name == 'INFO'):
            print(f"INFO: {message}")
        else :
            super().log(log_name, message)