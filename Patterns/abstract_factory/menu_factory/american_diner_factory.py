from .base import MenuFactory
from ..baked_goods.base import BakedGood
from ..drink.base import Drink
from ..baked_goods.muffin import Muffin
from ..drink.filter_coffee import FilterCoffee


class AmericanDinerFactory(MenuFactory):
    """Concrete Factory 2: American Diner Theme"""
    def create_baked_good(self) -> BakedGood:
        return Muffin()

    def create_drink(self) -> Drink:
        return FilterCoffee()
