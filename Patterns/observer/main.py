# file: /Users/deepanshumishra/Personal/LLD/Patterns/observer/main.py
from observer.observable.iphone import Iphone
from observer.observers.email import Email
from observer.observers.mobile import Mobile

def main():
    # Create the observable (subject)
    iphone_stock = Iphone()
    
    # Create observers
    email_observer1 = Email("user1@example.com", iphone_stock)
    email_observer2 = Email("user2@example.com", iphone_stock)
    mobile_observer = Mobile("john_doe", iphone_stock)
    
    # Register observers
    iphone_stock.add(email_observer1)
    iphone_stock.add(email_observer2)
    iphone_stock.add(mobile_observer)
    
    print("Initial stock: 0 (out of stock)")
    print("\n--- Setting stock to 10 ---")
    iphone_stock.set_stock_count(10)  # This will notify all observers
    
    print("\n--- Setting stock to 20 ---")
    iphone_stock.set_stock_count(20)  # No notification (already in stock)
    
    print("\n--- Setting stock to 0 ---")
    iphone_stock.set_stock_count(0)   # No notification (going out of stock)
    
    print("\n--- Setting stock to 5 ---")
    iphone_stock.set_stock_count(5)   # This will notify all observers again
    
    # Unregister an observer
    print("\n--- Removing email_observer1 ---")
    iphone_stock.remove(email_observer1)
    
    print("\n--- Setting stock to 0 then 15 ---")
    iphone_stock.set_stock_count(0)
    iphone_stock.set_stock_count(15)  # Only 2 observers will be notified

if __name__ == "__main__":
    main()