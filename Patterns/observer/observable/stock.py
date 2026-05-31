from abc import ABC, abstractmethod

class Stock(ABC):
    def add(self, observer) -> None:
        pass

    @abstractmethod
    def remove(self, observer) -> None:
        pass
    
    @abstractmethod
    def notify(self) -> None:
        """Notify all registered observers"""
        pass
    
    @abstractmethod
    def set_stock_count(self, new_stock: int) -> None:
        """Update stock count and notify if needed"""
        pass
    
    @abstractmethod
    def get_stock_count(self) -> int:
        """Get current stock count"""
        pass
