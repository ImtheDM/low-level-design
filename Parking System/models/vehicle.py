from ..constants import VehicleType

class Vehicle:
    def __init__(self, number, vehicle_type: VehicleType):
        self.vehicle_type = vehicle_type
        self.vehicle_number = number