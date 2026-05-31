from .stock import Stock
class Iphone(Stock):
    def __init__(self):
        self.observerList = []
        self.stockCount = 0

    def add(self, observer):
        self.observerList.append(observer)

    def remove(self, observer):
        self.observerList.remove(observer)

    def notify(self):
        for obs in self.observerList:
            obs.trigger()

    def set_stock_count(self, count : int):
        prev_count = self.get_stock_count()
        self.stockCount = count
        if(prev_count == 0):
            self.notify()
        self.stockCount = count

    def get_stock_count(self):
        return self.stockCount