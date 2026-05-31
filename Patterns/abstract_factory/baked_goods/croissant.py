from .base import BakedGood

class Croissant(BakedGood):
    def item_name(self) -> str:
        return "Croissant"
