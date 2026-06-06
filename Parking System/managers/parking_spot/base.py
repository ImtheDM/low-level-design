from ...models import ParkingSpot
from ...strategies.parking import ParkingStrategy, FirstAvailable


class ParkingSpotManager:

    def __init__(self, parking_strategy: ParkingStrategy = None):
        self.spots: list[ParkingSpot] = []  # overridden by subclasses
        self._parking_strategy = parking_strategy or FirstAvailable()

    def set_parking_strategy(self, strategy: ParkingStrategy):
        self._parking_strategy = strategy

    def add_spot(self, spot: ParkingSpot):
        self.spots.append(spot)

    def find_parking_space(self) -> ParkingSpot | None:
        return self._parking_strategy.find_space(self.spots)

    def add_vehicle(self, vehicle) -> ParkingSpot | None:
        spot = self.find_parking_space()
        if spot is None:
            return None
        spot.isEmpty = False
        spot.vehicle = vehicle
        return spot

    def remove_vehicle(self, spot: ParkingSpot):
        spot.isEmpty = True
        spot.vehicle = None
