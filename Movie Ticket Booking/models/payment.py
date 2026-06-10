from dataclasses import dataclass, field
from datetime import datetime
from constants import PaymentStatus


@dataclass
class Payment:
    id: str
    booking_id: str
    amount: float
    status: PaymentStatus = PaymentStatus.PENDING
    paid_at: datetime = None

    def mark_success(self):
        self.status = PaymentStatus.SUCCESS
        self.paid_at = datetime.now()

    def mark_failed(self):
        self.status = PaymentStatus.FAILED

    def refund(self):
        self.status = PaymentStatus.REFUNDED

    def __repr__(self):
        return f"Payment(₹{self.amount}, {self.status.value})"
