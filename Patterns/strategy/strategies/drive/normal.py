from .drive import DriveStrategy

class Normal(DriveStrategy):
    
    def drive(self):
        print("This is normal drive")