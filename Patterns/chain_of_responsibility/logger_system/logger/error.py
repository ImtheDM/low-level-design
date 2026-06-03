from .base import Logger

class Error(Logger):

    def __init__(self, next_handler=None):
        super().__init__(next_handler)

    def log(self, log_name, message):
        if(log_name == 'ERROR'):
            print(f"ERROR: {message}")
        else:
            super().log(log_name, message)