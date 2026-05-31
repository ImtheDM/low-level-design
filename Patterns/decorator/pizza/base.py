from abc import abstractmethod, ABC

class Pizza(ABC):

    @abstractmethod
    def cost(self):
        pass