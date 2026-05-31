from abc import ABC, abstractmethod

class BakedGood(ABC):

    @abstractmethod
    def item_name(self):
        pass
