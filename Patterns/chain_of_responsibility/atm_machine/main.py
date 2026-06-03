from currency_handler import TwoThousand, FiveHundred, TwoHundred, OneHundred


class ATM:
    """
    Builds a chain: ₹2000 → ₹500 → ₹200 → ₹100.
    note_counts: dict mapping denomination to available note count.
    """

    def __init__(self, note_counts: dict):
        hundred    = OneHundred(None,        note_counts.get(100, 0))
        two_hundred = TwoHundred(hundred,    note_counts.get(200, 0))
        five_hundred = FiveHundred(two_hundred, note_counts.get(500, 0))
        self.chain = TwoThousand(five_hundred, note_counts.get(2000, 0))

    def withdraw(self, amount: int):
        if amount <= 0:
            print("Enter a positive amount.")
            return
        if amount % 100 != 0:
            print(f"₹{amount} cannot be dispensed — minimum denomination is ₹100.")
            return
        print(f"\nWithdrawing ₹{amount}:")
        self.chain.fetch_money(amount)


if __name__ == "__main__":
    atm = ATM(note_counts={2000: 5, 500: 10, 200: 8, 100: 20})

    atm.withdraw(6800)   # 3×2000 + 1×500 + 1×200 + 1×100
    atm.withdraw(500)    # 1×500
    atm.withdraw(2300)   # 1×2000 + 1×200 + 1×100
    atm.withdraw(150)    # not a multiple of 100
    atm.withdraw(100000) # exceeds available notes
