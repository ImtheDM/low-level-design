from .base import CurrencyHandler


class FiveHundred(CurrencyHandler):

    DENOMINATION = 500

    def fetch_money(self, amount):
        self.dispatch(self.DENOMINATION, amount)
