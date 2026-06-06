from datetime import datetime


class Ticket:

    def __init__(self, parking_spot, vehicle):
        self.entry_time = datetime.now()
        self.exit_time = None
        self.parking_spot = parking_spot
        self.vehicle = vehicle
        self.cost = None

    def close(self, exit_time: datetime, cost: float):
        self.exit_time = exit_time
        self.cost = cost

    def __repr__(self):
        return (
            f"Ticket(vehicle={self.vehicle.vehicle_number}, "
            f"spot={self.parking_spot.id}, "
            f"entry={self.entry_time.strftime('%H:%M:%S')}, "
            f"exit={self.exit_time.strftime('%H:%M:%S') if self.exit_time else 'open'}, "
            f"cost={self.cost})"
        )
