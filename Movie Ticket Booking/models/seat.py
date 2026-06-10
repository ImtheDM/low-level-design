from dataclasses import dataclass
from constants import SeatType


@dataclass
class Seat:
    id: str
    screen_id: str
    row: str
    col: int
    seat_type: SeatType
    base_price: float

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Seat) and self.id == other.id

    def __repr__(self):
        return f"Seat({self.row}{self.col}, {self.seat_type.value}, ₹{self.base_price})"
