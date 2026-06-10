from abc import ABC, abstractmethod
from typing import List
from models.seat import Seat
from constants import SeatStatus


class SeatSelectionStrategy(ABC):
    @abstractmethod
    def select(self, available_seats: List[Seat], count: int) -> List[Seat]:
        pass


class BestAvailable(SeatSelectionStrategy):
    """Picks `count` contiguous seats in the same row, closest to the middle."""

    def select(self, available_seats: List[Seat], count: int) -> List[Seat]:
        by_row: dict[str, List[Seat]] = {}
        for seat in available_seats:
            by_row.setdefault(seat.row, []).append(seat)

        for row_seats in by_row.values():
            row_seats.sort(key=lambda s: s.col)
            for i in range(len(row_seats) - count + 1):
                group = row_seats[i:i + count]
                if [s.col for s in group] == list(range(group[0].col, group[0].col + count)):
                    return group

        # fallback: return any `count` seats if no contiguous group found
        if len(available_seats) >= count:
            return available_seats[:count]
        raise ValueError(f"Not enough available seats. Requested {count}, found {len(available_seats)}.")


class CheapestFirst(SeatSelectionStrategy):
    """Picks the cheapest `count` available seats."""

    def select(self, available_seats: List[Seat], count: int) -> List[Seat]:
        if len(available_seats) < count:
            raise ValueError(f"Not enough available seats. Requested {count}, found {len(available_seats)}.")
        return sorted(available_seats, key=lambda s: s.base_price)[:count]
