from abc import ABC, abstractmethod


class ParkingStrategy(ABC):

    @abstractmethod
    def find_space(self, spots: list) -> object | None:
        pass


class FirstAvailable(ParkingStrategy):
    """Returns the first free spot in insertion order."""

    def find_space(self, spots: list) -> object | None:
        for spot in spots:
            if spot.isEmpty:
                return spot
        return None


class NearestToEntrance(ParkingStrategy):
    """Returns the free spot with the lexicographically smallest location."""

    def find_space(self, spots: list) -> object | None:
        available = [s for s in spots if s.isEmpty]
        if not available:
            return None
        return min(available, key=lambda s: s.location)


class LowestPrice(ParkingStrategy):
    """Returns the free spot with the lowest price per unit."""

    def find_space(self, spots: list) -> object | None:
        available = [s for s in spots if s.isEmpty]
        if not available:
            return None
        return min(available, key=lambda s: s.price)
