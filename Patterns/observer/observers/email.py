from .alert_observer import AlertObserver

class Email(AlertObserver):
    def __init__(self, email, observable):
        self.email = email
        self.observable = observable

    def trigger(self):
        stock_count = self.observable.get_stock_count()
        self.send_email(stock_count)


    def send_email(self, stock_count):
        print(f"Email sent to {self.email}: Produce back in stock: Count {stock_count}")