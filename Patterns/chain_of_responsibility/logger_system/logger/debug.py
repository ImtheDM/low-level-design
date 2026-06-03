from .base import Logger

class Debug(Logger):

    def __init__(self, next_handler=None):
        super().__init__(next_handler)

    def log(self, log_name, message):
        if(log_name == 'DEBUG'):
            print(f"DEBUG: {message}")
        else:
            super().log(log_name, message)