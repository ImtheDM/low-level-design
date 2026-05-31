from .alert_observer import AlertObserver

class Mobile(AlertObserver):
    def __init__(self, number, observable):
        self.number = number
        self.observable = observable

    def trigger(self):
        stock_count = self.observable.get_stock_count()
        self.send_notification(stock_count)


    def send_notification(self, stock_count):
        print(f"Notification sent to {self.number}: Produce back in stock: Count {stock_count}")