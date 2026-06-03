from .base import CurrencyHandler


class TwoHundred(CurrencyHandler):

    DENOMINATION = 200

    def fetch_money(self, amount):
        self.dispatch(self.DENOMINATION, amount)
