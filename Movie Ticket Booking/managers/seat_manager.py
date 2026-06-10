import threading
import time
from typing import List, Dict, Tuple
from models.show import Show
from models.seat import Seat
from constants import SeatStatus

LOCK_TTL_SECONDS = 600  # 10-minute lock expiry


class SeatUnavailableError(Exception):
    pass


class SeatManager:
    """
    Manages seat status transitions with per-show locking.

    State machine:  AVAILABLE → LOCKED → BOOKED
                                LOCKED → AVAILABLE  (on expiry or failed payment)
                    BOOKED    → AVAILABLE            (on cancellation)
    """

    def __init__(self):
        # show_id -> Lock  (fine-grained: one lock per show, not a global lock)
        self._locks: Dict[str, threading.Lock] = {}
        # (show_id, seat_id) -> lock_expiry_timestamp
        self._lock_expiry: Dict[Tuple[str, str], float] = {}

    def _get_lock(self, show_id: str) -> threading.Lock:
        if show_id not in self._locks:
            self._locks[show_id] = threading.Lock()
        return self._locks[show_id]

    def _is_expired(self, show_id: str, seat_id: str) -> bool:
        key = (show_id, seat_id)
        expiry = self._lock_expiry.get(key)
        return expiry is not None and time.time() > expiry

    def get_available_seats(self, show: Show, seats: List[Seat]) -> List[Seat]:
        with self._get_lock(show.id):
            available = []
            for seat in seats:
                status = show.seat_status.get(seat.id)
                if status == SeatStatus.AVAILABLE:
                    available.append(seat)
                elif status == SeatStatus.LOCKED and self._is_expired(show.id, seat.id):
                    # auto-release expired lock
                    show.seat_status[seat.id] = SeatStatus.AVAILABLE
                    self._lock_expiry.pop((show.id, seat.id), None)
                    available.append(seat)
            return available

    def lock_seats(self, show: Show, seats: List[Seat], user_id: str) -> None:
        """
        Atomically checks availability and locks all requested seats.
        Raises SeatUnavailableError if any seat is taken or locked by another user.
        """
        with self._get_lock(show.id):
            now = time.time()
            for seat in seats:
                status = show.seat_status.get(seat.id)
                if status == SeatStatus.LOCKED and self._is_expired(show.id, seat.id):
                    show.seat_status[seat.id] = SeatStatus.AVAILABLE
                    self._lock_expiry.pop((show.id, seat.id), None)
                    status = SeatStatus.AVAILABLE
                if status != SeatStatus.AVAILABLE:
                    raise SeatUnavailableError(
                        f"Seat {seat.id} is {status.value}. Please choose different seats."
                    )
            # all seats available — flip them atomically
            for seat in seats:
                show.seat_status[seat.id] = SeatStatus.LOCKED
                self._lock_expiry[(show.id, seat.id)] = now + LOCK_TTL_SECONDS

    def confirm_seats(self, show: Show, seats: List[Seat]) -> None:
        with self._get_lock(show.id):
            for seat in seats:
                show.seat_status[seat.id] = SeatStatus.BOOKED
                self._lock_expiry.pop((show.id, seat.id), None)

    def release_seats(self, show: Show, seats: List[Seat]) -> None:
        """Release locked or booked seats back to AVAILABLE (used on cancel / payment failure)."""
        with self._get_lock(show.id):
            for seat in seats:
                show.seat_status[seat.id] = SeatStatus.AVAILABLE
                self._lock_expiry.pop((show.id, seat.id), None)
