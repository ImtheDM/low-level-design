from .vehicle import Sports, Offroad, Passenger
from .strategies.drive.sporty import Sporty
from .strategies.drive.normal import Normal

if __name__ == "__main__":
    monster_truck = Offroad(Sporty())
    bus = Passenger(Normal())
    ferrari = Sports(Sporty())

    monster_truck.drive()
    bus.drive()
    ferrari.drive()