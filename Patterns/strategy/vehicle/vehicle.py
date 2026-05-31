from ..strategies.drive.drive import DriveStrategy

class Vehicle:
    def __init__(self, drive_strategy: DriveStrategy):
        self._drive_strategy = drive_strategy

    def drive(self):
        self._drive_strategy.drive()