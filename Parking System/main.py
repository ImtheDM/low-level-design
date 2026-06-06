import time

from constants import VehicleType
from models import Vehicle, ParkingSpot
from managers.parking_spot.parking_spot_factory import ParkingSpotFactory
from managers.entrance_gate import EntranceGate
from managers.exit_gate import ExitGate
from strategies import HourlyCost, MinuteCost, NearestToEntrance, LowestPrice


def build_lot(factory: ParkingSpotFactory):
    two_w = factory.fetch_manager(VehicleType.TWO_WHEELER)
    two_w.add_spot(ParkingSpot(id="2W-1", vehicle_type=VehicleType.TWO_WHEELER, location="C3", price=20))
    two_w.add_spot(ParkingSpot(id="2W-2", vehicle_type=VehicleType.TWO_WHEELER, location="A1", price=25))
    two_w.add_spot(ParkingSpot(id="2W-3", vehicle_type=VehicleType.TWO_WHEELER, location="B2", price=15))

    four_w = factory.fetch_manager(VehicleType.FOUR_WHEELER)
    four_w.add_spot(ParkingSpot(id="4W-1", vehicle_type=VehicleType.FOUR_WHEELER, location="D4", price=80))
    four_w.add_spot(ParkingSpot(id="4W-2", vehicle_type=VehicleType.FOUR_WHEELER, location="B1", price=50))
    four_w.add_spot(ParkingSpot(id="4W-3", vehicle_type=VehicleType.FOUR_WHEELER, location="A2", price=60))


def main():
    print("=" * 50)
    print("SCENARIO 1 — FirstAvailable + Hourly pricing")
    print("=" * 50)
    factory = ParkingSpotFactory()  # defaults to FirstAvailable for both
    build_lot(factory)
    entrance = EntranceGate(factory)
    exit_gate = ExitGate(factory, HourlyCost())

    bike = Vehicle(number="MH-01-AB-1234", vehicle_type=VehicleType.TWO_WHEELER)
    ticket = entrance.check_in(bike)   # expects spot 2W-1 (first inserted)
    time.sleep(1)
    exit_gate.check_out(ticket)
    print(ticket)

    print()
    print("=" * 50)
    print("SCENARIO 2 — NearestToEntrance + Minute pricing (four-wheeler)")
    print("=" * 50)
    factory2 = ParkingSpotFactory(four_wheeler_strategy=NearestToEntrance())
    build_lot(factory2)
    entrance2 = EntranceGate(factory2)
    exit_gate2 = ExitGate(factory2, MinuteCost())

    car = Vehicle(number="MH-02-CD-5678", vehicle_type=VehicleType.FOUR_WHEELER)
    ticket2 = entrance2.check_in(car)  # expects spot 4W-3 (location A2, nearest)
    time.sleep(1)
    exit_gate2.check_out(ticket2)
    print(ticket2)

    print()
    print("=" * 50)
    print("SCENARIO 3 — LowestPrice strategy (two-wheeler)")
    print("=" * 50)
    factory3 = ParkingSpotFactory(two_wheeler_strategy=LowestPrice())
    build_lot(factory3)
    entrance3 = EntranceGate(factory3)
    exit_gate3 = ExitGate(factory3, HourlyCost())

    bike2 = Vehicle(number="MH-03-EF-9999", vehicle_type=VehicleType.TWO_WHEELER)
    ticket3 = entrance3.check_in(bike2)  # expects spot 2W-3 (price ₹15, cheapest)
    time.sleep(1)
    exit_gate3.check_out(ticket3)
    print(ticket3)

    print()
    print("=" * 50)
    print("SCENARIO 4 — Switch parking strategy at runtime")
    print("=" * 50)
    two_w_manager = factory3.fetch_manager(VehicleType.TWO_WHEELER)
    two_w_manager.set_parking_strategy(NearestToEntrance())

    bike3 = Vehicle(number="MH-04-GH-0000", vehicle_type=VehicleType.TWO_WHEELER)
    ticket4 = entrance3.check_in(bike3)  # now uses NearestToEntrance
    time.sleep(1)
    exit_gate3.check_out(ticket4)
    print(ticket4)

    print()
    print("=" * 50)
    print("SCENARIO 5 — No available spot (lot full)")
    print("=" * 50)
    try:
        bike4 = Vehicle(number="MH-05-IJ-1111", vehicle_type=VehicleType.TWO_WHEELER)
        entrance3.check_in(bike4)   # all 3 two-wheeler spots taken
    except Exception as e:
        print(f"[Expected error] {e}")


if __name__ == "__main__":
    main()
