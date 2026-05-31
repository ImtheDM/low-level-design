from abc import ABC, abstractmethod
from ..baked_goods.base import BakedGood
from ..drink.base import Drink


class MenuFactory(ABC):
    """Abstract Factory that enforces a matching food + drink pairing."""
    @abstractmethod
    def create_baked_good(self) -> BakedGood: pass

    @abstractmethod
    def create_drink(self) -> Drink: pass
