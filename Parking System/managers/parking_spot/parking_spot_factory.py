from .two_wheeler import TwoWheelerManager
from .four_wheeler import FourWheelerManager
from ...constants import VehicleType
from ...strategies.parking import ParkingStrategy


class ParkingSpotFactory:

    def __init__(
        self,
        two_wheeler_strategy: ParkingStrategy = None,
        four_wheeler_strategy: ParkingStrategy = None,
    ):
        self._managers = {
            VehicleType.TWO_WHEELER: TwoWheelerManager(two_wheeler_strategy),
            VehicleType.FOUR_WHEELER: FourWheelerManager(four_wheeler_strategy),
        }

    def fetch_manager(self, vehicle_type: VehicleType):
        manager = self._managers.get(vehicle_type)
        if manager is None:
            raise ValueError(f"No manager found for {vehicle_type}")
        return manager
