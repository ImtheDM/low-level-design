from .base import ToppingsDecorator

class Mushrooms(ToppingsDecorator):


    def cost(self):
        return self.pizza.cost() + 5