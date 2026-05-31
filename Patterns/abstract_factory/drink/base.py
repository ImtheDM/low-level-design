from abc import ABC, abstractmethod

class Drink(ABC):
    @abstractmethod
    def drink_type(self) -> str: pass
