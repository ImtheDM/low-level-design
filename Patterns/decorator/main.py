from pizza import Farmhouse, Mushrooms, Margherita, ExtraCheese

if __name__ == "__main__":
    print("--- Welcome to the Python Pizza Machine ---\n")

    # Order 1: A simple Thin Crust with Extra Cheese
    order_1 = Farmhouse()
    order_1 = ExtraCheese(order_1)
    
    print(f"Total Cost: ${order_1.cost():.2f}\n")

    # Order 2: A loaded Thick Crust Pizza
    # Look how we can stack them instantly!
    order_2 = Margherita()
    order_2 = ExtraCheese(order_2)
    order_2 = Mushrooms(order_2)

    print(f"Total Cost: ${order_2.cost():.2f}\n")