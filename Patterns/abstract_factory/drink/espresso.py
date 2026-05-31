from .base import Drink

class Espresso(Drink):
    def drink_type(self) -> str: return "Strong Espresso"
