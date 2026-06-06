from .base import ParkingSpotManager
from ...constants import VehicleType
from ...models import ParkingSpot

class FourWheelerManager(ParkingSpotManager):

    VEHICLE_TYPE = VehicleType.FOUR_WHEELER

    def __init__(self, parking_strategy=None):
        super().__init__(parking_strategy)
        self.spots: list[ParkingSpot] = []

    def add_vehicle(self, vehicle):
        if vehicle.vehicle_type != self.VEHICLE_TYPE:
            raise ValueError(f"FourWheelerManager only accepts FOUR_WHEELER vehicles")
        return super().add_vehicle(vehicle)
