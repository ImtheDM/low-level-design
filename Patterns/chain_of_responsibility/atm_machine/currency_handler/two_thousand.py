from .base import CurrencyHandler


class TwoThousand(CurrencyHandler):

    DENOMINATION = 2000

    def fetch_money(self, amount):
        self.dispatch(self.DENOMINATION, amount)
