from .menu_factory import MenuFactory, FrenchCafeFactory, AmericanDinerFactory


def serve_breakfast(factory: MenuFactory):
    """The client handles the theme uniformly."""
    food = factory.create_baked_good()
    drink = factory.create_drink()
    print(f"Serving {food.__class__.__name__} with a side of {drink.drink_type()}!")


if __name__ == "__main__":
    # Let's run a French Cafe morning
    serve_breakfast(FrenchCafeFactory())
    # Output: Serving Croissant with a side of Strong Espresso!

    # Switch the whole theme instantly
    serve_breakfast(AmericanDinerFactory())
    # Output: Serving Muffin with a side of Drip Filter Coffee!
