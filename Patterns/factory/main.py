from .backery_factory import BakeryFactory

if __name__ == "__main__":
    
    croissant = BakeryFactory.get_food("croissant")
    muffin = BakeryFactory.get_food("muffin")

    print(f"I have got a {croissant.item_name()}")
    print(f"I have got a {muffin.item_name()}")