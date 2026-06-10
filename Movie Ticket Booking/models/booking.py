from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from .seat import Seat
from .show import Show
from .payment import Payment
from constants import BookingStatus


@dataclass
class Booking:
    id: str
    user_id: str
    show: Show
    seats: List[Seat]
    status: BookingStatus = BookingStatus.PENDING
    payment: Payment = None
    created_at: datetime = field(default_factory=datetime.now)

    def confirm(self, payment: Payment):
        self.payment = payment
        self.status = BookingStatus.CONFIRMED

    def cancel(self):
        self.status = BookingStatus.CANCELLED
        if self.payment:
            self.payment.refund()

    def __repr__(self):
        seats = ", ".join(str(s) for s in self.seats)
        return (
            f"Booking(id={self.id}, user={self.user_id}, show={self.show}, "
            f"seats=[{seats}], status={self.status.value}, payment={self.payment})"
        )
