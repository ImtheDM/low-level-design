from .croissant import Croissant
from .muffin import Muffin

class BakeryFactory:

    @staticmethod
    def get_food(item_name):
        if item_name == "croissant":
            return Croissant()
        elif item_name == "muffin":
            return Muffin()
        else:
            print("Food not available")
            return None
