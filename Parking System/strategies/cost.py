from abc import ABC, abstractmethod
from datetime import datetime
import math


class CostStrategy(ABC):

    @abstractmethod
    def compute(self, entry_time: datetime, exit_time: datetime, price_per_unit: float) -> float:
        pass


class HourlyCost(CostStrategy):

    def compute(self, entry_time: datetime, exit_time: datetime, price_per_unit: float) -> float:
        elapsed_seconds = (exit_time - entry_time).total_seconds()
        hours = math.ceil(elapsed_seconds / 3600)  # round up to next hour
        return hours * price_per_unit


class MinuteCost(CostStrategy):

    def compute(self, entry_time: datetime, exit_time: datetime, price_per_unit: float) -> float:
        elapsed_seconds = (exit_time - entry_time).total_seconds()
        minutes = math.ceil(elapsed_seconds / 60)  # round up to next minute
        return minutes * price_per_unit
