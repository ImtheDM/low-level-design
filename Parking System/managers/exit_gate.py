from datetime import datetime

from ..models import Ticket
from ..strategies import CostStrategy
from ..managers.parking_spot.parking_spot_factory import ParkingSpotFactory


class ExitGate:

    def __init__(self, factory: ParkingSpotFactory, cost_strategy: CostStrategy):
        self._factory = factory
        self._cost_strategy = cost_strategy

    def set_cost_strategy(self, strategy: CostStrategy):
        """Swap pricing strategy at runtime."""
        self._cost_strategy = strategy

    def check_out(self, ticket: Ticket) -> float:
        exit_time = datetime.now()
        price_per_unit = ticket.parking_spot.price
        cost = self._cost_strategy.compute(ticket.entry_time, exit_time, price_per_unit)

        manager = self._factory.fetch_manager(ticket.vehicle.vehicle_type)
        manager.remove_vehicle(ticket.parking_spot)

        ticket.close(exit_time, cost)
        print(f"[ExitGate] {ticket.vehicle.vehicle_number} checked out → cost ₹{cost:.2f}")
        return cost
