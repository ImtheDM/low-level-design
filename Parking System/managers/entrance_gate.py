from ..models import Ticket, Vehicle
from ..managers.parking_spot.parking_spot_factory import ParkingSpotFactory


class EntranceGate:

    def __init__(self, factory: ParkingSpotFactory):
        self._factory = factory

    def check_in(self, vehicle: Vehicle) -> Ticket:
        manager = self._factory.fetch_manager(vehicle.vehicle_type)
        spot = manager.add_vehicle(vehicle)
        if spot is None:
            raise Exception(f"No available spot for {vehicle.vehicle_type.value}")
        ticket = Ticket(parking_spot=spot, vehicle=vehicle)
        print(f"[EntranceGate] {vehicle.vehicle_number} checked in → spot {spot.id}")
        return ticket
