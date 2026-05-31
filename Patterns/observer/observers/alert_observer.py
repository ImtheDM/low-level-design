from abc import ABC, abstractmethod

class AlertObserver(ABC):

    @abstractmethod
    def trigger(self):
        pass