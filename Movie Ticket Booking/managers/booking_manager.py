import uuid
from typing import List
from models.show import Show
from models.seat import Seat
from models.booking import Booking
from models.payment import Payment
from managers.show_manager import ShowManager
from managers.seat_manager import SeatManager, SeatUnavailableError
from strategies.seat_selection import SeatSelectionStrategy, BestAvailable
from strategies.pricing import PricingStrategy, BasePricing
from constants import BookingStatus


class BookingManager:
    def __init__(
        self,
        show_manager: ShowManager,
        seat_manager: SeatManager,
        seat_strategy: SeatSelectionStrategy = None,
        pricing_strategy: PricingStrategy = None,
    ):
        self._show_manager = show_manager
        self._seat_manager = seat_manager
        self._seat_strategy = seat_strategy or BestAvailable()
        self._pricing_strategy = pricing_strategy or BasePricing()
        self._bookings: dict[str, Booking] = {}

    def book(self, user_id: str, show: Show, seat_count: int) -> Booking:
        all_seats = self._show_manager.get_seats_for_screen(show.screen.id)
        available = self._seat_manager.get_available_seats(show, all_seats)
        selected = self._seat_strategy.select(available, seat_count)

        # lock atomically — raises SeatUnavailableError if race is lost
        self._seat_manager.lock_seats(show, selected, user_id)

        booking_id = str(uuid.uuid4())[:8]
        amount = self._pricing_strategy.compute(selected, show.start_time)
        payment = Payment(id=str(uuid.uuid4())[:8], booking_id=booking_id, amount=amount)
        booking = Booking(id=booking_id, user_id=user_id, show=show, seats=selected)
        self._bookings[booking_id] = booking
        return booking

    def confirm_payment(self, booking: Booking) -> Booking:
        """Simulate successful payment and confirm the booking."""
        if booking.status != BookingStatus.PENDING:
            raise ValueError(f"Booking {booking.id} is not in PENDING state.")

        amount = self._pricing_strategy.compute(booking.seats, booking.show.start_time)
        payment = Payment(id=str(uuid.uuid4())[:8], booking_id=booking.id, amount=amount)
        payment.mark_success()

        self._seat_manager.confirm_seats(booking.show, booking.seats)
        booking.confirm(payment)
        return booking

    def cancel_booking(self, booking: Booking) -> Booking:
        if booking.status == BookingStatus.CANCELLED:
            raise ValueError(f"Booking {booking.id} is already cancelled.")
        self._seat_manager.release_seats(booking.show, booking.seats)
        booking.cancel()
        return booking

    def fail_payment(self, booking: Booking) -> None:
        """Release locks when payment fails."""
        self._seat_manager.release_seats(booking.show, booking.seats)
        if booking.payment:
            booking.payment.mark_failed()
        booking.status = BookingStatus.CANCELLED
