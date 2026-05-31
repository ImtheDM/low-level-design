from .base import Drink

class FilterCoffee(Drink):
    def drink_type(self) -> str: return "Drip Filter Coffee"