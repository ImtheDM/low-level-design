from .base import CurrencyHandler


class OneHundred(CurrencyHandler):

    DENOMINATION = 100

    def fetch_money(self, amount):
        self.dispatch(self.DENOMINATION, amount)
