from enum import Enum


class City(Enum):
    MUMBAI = "Mumbai"
    DELHI = "Delhi"
    BANGALORE = "Bangalore"
    HYDERABAD = "Hyderabad"
    PUNE = "Pune"


class SeatType(Enum):
    RECLINER = "Recliner"
    PREMIUM = "Premium"
    STANDARD = "Standard"


class SeatStatus(Enum):
    AVAILABLE = "Available"
    LOCKED = "Locked"
    BOOKED = "Booked"


class BookingStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"


class PaymentStatus(Enum):
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"
    REFUNDED = "Refunded"
