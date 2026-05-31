from abc import abstractmethod, ABC
from ..base import Pizza

class ToppingsDecorator(Pizza, ABC):

    def __init__(self, pizza: Pizza):
        self.pizza = pizza

    @abstractmethod
    def cost(self):
        pass