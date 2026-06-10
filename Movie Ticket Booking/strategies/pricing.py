from abc import ABC, abstractmethod
from datetime import datetime
from typing import List
from models.seat import Seat


class PricingStrategy(ABC):
    @abstractmethod
    def compute(self, seats: List[Seat], show_time: datetime) -> float:
        pass


class BasePricing(PricingStrategy):
    """Total = sum of each seat's base price."""

    def compute(self, seats: List[Seat], show_time: datetime) -> float:
        return sum(s.base_price for s in seats)


class WeekendSurcharge(PricingStrategy):
    """Adds 20% surcharge on Saturdays and Sundays."""

    SURCHARGE = 0.20

    def compute(self, seats: List[Seat], show_time: datetime) -> float:
        total = sum(s.base_price for s in seats)
        if show_time.weekday() >= 5:  # 5=Saturday, 6=Sunday
            total *= (1 + self.SURCHARGE)
        return round(total, 2)
