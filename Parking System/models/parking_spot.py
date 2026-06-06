from ..constants import VehicleType

class ParkingSpot:

    def __init__(self, id, vehicle_type: VehicleType, location, price):
        self.id = id
        self.isEmpty = True
        self.vehicle_type = vehicle_type
        self.vehicle = None
        self.location = location
        self.price = price
