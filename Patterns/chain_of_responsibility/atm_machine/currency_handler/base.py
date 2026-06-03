from abc import ABC, abstractmethod


class CurrencyHandler(ABC):

    def __init__(self, next_handler, note_count):
        self.next_handler = next_handler
        self.note_count = note_count

    @abstractmethod
    def fetch_money(self, amount):
        pass

    def dispatch(self, denomination, amount):
        notes_to_give = min(amount // denomination, self.note_count)
        remaining = amount - notes_to_give * denomination

        if notes_to_give > 0:
            print(f"  Dispensing {notes_to_give} x ₹{denomination}")

        if remaining == 0:
            print("Successfully withdrawn!")
        elif self.next_handler:
            self.next_handler.fetch_money(remaining)
        else:
            print(f"Cannot dispense ₹{remaining} — insufficient notes or unsupported denomination")
