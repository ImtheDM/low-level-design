from .base import ToppingsDecorator

class ExtraCheese(ToppingsDecorator):


    def cost(self):
        return self.pizza.cost() + 10