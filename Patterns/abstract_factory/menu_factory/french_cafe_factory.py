from .base import MenuFactory
from ..baked_goods.base import BakedGood
from ..drink.base import Drink
from ..baked_goods.croissant import Croissant
from ..drink.espresso import Espresso


class FrenchCafeFactory(MenuFactory):
    """Concrete Factory 1: French Cafe Theme"""
    def create_baked_good(self) -> BakedGood:
        return Croissant()

    def create_drink(self) -> Drink:
        return Espresso()
