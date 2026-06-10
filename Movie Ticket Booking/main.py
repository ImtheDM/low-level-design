import threading
import time
from datetime import datetime

from constants import City, SeatType
from models import Movie, Theatre, Screen, Seat, Show, User
from managers import ShowManager, SeatManager, BookingManager
from managers.seat_manager import SeatUnavailableError
from strategies import BestAvailable, CheapestFirst, BasePricing, WeekendSurcharge


# ── helpers ──────────────────────────────────────────────────────────────────

def build_screen_seats(screen: Screen) -> list[Seat]:
    seats = []
    for row in ["A", "B", "C"]:
        for col in range(1, 6):
            if row == "A":
                seat_type, price = SeatType.RECLINER, 500.0
            elif row == "B":
                seat_type, price = SeatType.PREMIUM, 300.0
            else:
                seat_type, price = SeatType.STANDARD, 150.0
            seats.append(Seat(
                id=f"{screen.id}-{row}{col}",
                screen_id=screen.id,
                row=row, col=col,
                seat_type=seat_type,
                base_price=price,
            ))
    return seats


def divider(title: str):
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


# ── seed data ─────────────────────────────────────────────────────────────────

def seed(show_manager: ShowManager):
    # Movies
    interstellar = Movie("M1", "Interstellar", 169, "Sci-Fi", "English")
    pathaan      = Movie("M2", "Pathaan",       146, "Action", "Hindi")
    leo          = Movie("M3", "Leo",            164, "Action", "Tamil")

    # Theatres
    pvr_mumbai    = Theatre("T1", "PVR Juhu",      City.MUMBAI,    "Juhu, Mumbai")
    inox_mumbai   = Theatre("T2", "INOX Nariman",  City.MUMBAI,    "Nariman Point, Mumbai")
    pvr_delhi     = Theatre("T3", "PVR Select",    City.DELHI,     "Select Citywalk, Delhi")
    cinepolis_blr = Theatre("T4", "Cinepolis Orion", City.BANGALORE, "Orion Mall, Bangalore")

    # Screens
    s1 = Screen("S1", "Audi 1", pvr_mumbai,    10, 10)
    s2 = Screen("S2", "Audi 1", inox_mumbai,   10, 10)
    s3 = Screen("S3", "Audi 1", pvr_delhi,     10, 10)
    s4 = Screen("S4", "Audi 1", cinepolis_blr, 10, 10)

    # Register seats per screen
    for screen in [s1, s2, s3, s4]:
        show_manager.register_seats(screen, build_screen_seats(screen))

    # Shows  (Saturday show → weekend surcharge)
    saturday = datetime(2026, 6, 7, 18, 30)   # Saturday 6:30 PM
    weekday  = datetime(2026, 6, 10, 15, 0)   # Tuesday  3:00 PM

    shows = [
        Show("SH1", interstellar, s1, saturday),   # Mumbai, PVR Juhu
        Show("SH2", interstellar, s2, weekday),    # Mumbai, INOX Nariman
        Show("SH3", pathaan,      s1, saturday),   # Mumbai, PVR Juhu
        Show("SH4", interstellar, s3, saturday),   # Delhi,  PVR Select
        Show("SH5", leo,          s4, weekday),    # Bangalore
    ]
    for show in shows:
        show_manager.register_show(show)

    return interstellar, pathaan, leo


# ── scenarios ────────────────────────────────────────────────────────────────

def scenario_city_browsing(show_manager: ShowManager, interstellar, pathaan):
    divider("SCENARIO 1 — City-level browsing")

    for city in [City.MUMBAI, City.DELHI, City.BANGALORE, City.PUNE]:
        movies = show_manager.get_movies_by_city(city)
        print(f"\n{city.value}: {[m.title for m in movies] or 'No shows'}")

    print("\n--- Theatres showing Interstellar in Mumbai ---")
    theatres = show_manager.get_theatres_by_city_and_movie(City.MUMBAI, interstellar)
    for t in theatres:
        shows = show_manager.get_shows_by_theatre_and_movie(t, interstellar)
        print(f"  {t.name}: {[str(s) for s in shows]}")


def scenario_normal_booking(show_manager: ShowManager, booking_manager: BookingManager, interstellar):
    divider("SCENARIO 2 — Normal booking (BestAvailable + BasePricing)")

    show = show_manager.get_show_by_id("SH1")
    booking = booking_manager.book(user_id="U1", show=show, seat_count=2)
    print(f"Locked:    {booking}")

    booking_manager.confirm_payment(booking)
    print(f"Confirmed: {booking}")


def scenario_weekend_surcharge(show_manager: ShowManager, booking_manager: BookingManager):
    divider("SCENARIO 3 — Weekend surcharge (20% on Saturday show)")

    show = show_manager.get_show_by_id("SH4")  # Delhi, Saturday
    weekend_mgr = BookingManager(
        show_manager, SeatManager(),
        seat_strategy=CheapestFirst(),
        pricing_strategy=WeekendSurcharge(),
    )
    booking = weekend_mgr.book(user_id="U2", show=show, seat_count=3)
    weekend_mgr.confirm_payment(booking)
    print(f"Weekend booking: {booking}")
    expected_base = 3 * 150.0  # 3 Standard seats
    print(f"  Base: ₹{expected_base}  →  With 20% surcharge: ₹{booking.payment.amount}")


def scenario_cancellation(show_manager: ShowManager, booking_manager: BookingManager):
    divider("SCENARIO 4 — Cancellation releases seats")

    show = show_manager.get_show_by_id("SH2")
    all_seats = show_manager.get_seats_for_screen(show.screen.id)
    seat_manager = booking_manager._seat_manager

    booking = booking_manager.book(user_id="U3", show=show, seat_count=2)
    booking_manager.confirm_payment(booking)
    print(f"Booked:    {booking}")

    from constants import SeatStatus
    seat_ids = [s.id for s in booking.seats]
    print(f"  Status before cancel: {[show.seat_status[sid].value for sid in seat_ids]}")

    booking_manager.cancel_booking(booking)
    print(f"Cancelled: {booking}")
    print(f"  Status after cancel:  {[show.seat_status[sid].value for sid in seat_ids]}")


def scenario_concurrency(show_manager: ShowManager):
    divider("SCENARIO 5 — Concurrent booking race (2 users, same seats)")

    # Build a dedicated show with only 3 seats so both users must compete for the same group.
    pvr_mumbai = Theatre("T1", "PVR Juhu", City.MUMBAI, "Juhu, Mumbai")
    screen = Screen("S_RACE", "Race Audi", pvr_mumbai, 1, 3)
    three_seats = [
        Seat(f"S_RACE-A{c}", "S_RACE", "A", c, SeatType.PREMIUM, 300.0)
        for c in range(1, 4)
    ]
    show_manager.register_seats(screen, three_seats)
    from models import Movie as _Movie
    race_movie = _Movie("M_RACE", "Race Show", 120, "Test", "English")
    race_show  = Show("SH_RACE", race_movie, screen, datetime(2026, 6, 7, 20, 0))
    show_manager.register_show(race_show)

    seat_manager   = SeatManager()
    booking_manager = BookingManager(show_manager, seat_manager)
    results = {}

    barrier = threading.Barrier(2)  # ensure both threads enter lock_seats simultaneously

    def user_thread(user_id: str):
        try:
            all_seats = show_manager.get_seats_for_screen(race_show.screen.id)
            available = seat_manager.get_available_seats(race_show, all_seats)
            selected  = BestAvailable().select(available, 3)
            barrier.wait()  # both threads reach here before either grabs the lock
            seat_manager.lock_seats(race_show, selected, user_id)
            seat_manager.confirm_seats(race_show, selected)
            results[user_id] = f"SUCCESS — booked seats {[s.id for s in selected]}"
        except SeatUnavailableError as e:
            results[user_id] = f"FAILED  — {e}"

    t1 = threading.Thread(target=user_thread, args=("Alice",))
    t2 = threading.Thread(target=user_thread, args=("Bob",))
    t1.start(); t2.start()
    t1.join();  t2.join()

    for user, result in results.items():
        print(f"  {user:6s}: {result}")
    print("\n  → Exactly one user succeeded; the other received SeatUnavailableError.")


def scenario_payment_failure(show_manager: ShowManager):
    divider("SCENARIO 6 — Payment failure releases locked seats")

    show = show_manager.get_show_by_id("SH5")  # Bangalore, Leo
    seat_manager = SeatManager()
    booking_manager = BookingManager(show_manager, seat_manager)

    booking = booking_manager.book(user_id="U5", show=show, seat_count=2)
    seat_ids = [s.id for s in booking.seats]
    from constants import SeatStatus
    print(f"  After lock:   {[show.seat_status[sid].value for sid in seat_ids]}")

    booking_manager.fail_payment(booking)
    print(f"  After failure: {[show.seat_status[sid].value for sid in seat_ids]}")
    print(f"  Booking status: {booking.status.value}")

    # same seats can now be booked again
    booking2 = booking_manager.book(user_id="U6", show=show, seat_count=2)
    booking_manager.confirm_payment(booking2)
    print(f"  Re-booked successfully: {booking2.status.value}")


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    show_manager  = ShowManager()
    seat_manager  = SeatManager()
    booking_manager = BookingManager(show_manager, seat_manager)

    interstellar, pathaan, leo = seed(show_manager)

    scenario_city_browsing(show_manager, interstellar, pathaan)
    scenario_normal_booking(show_manager, booking_manager, interstellar)
    scenario_weekend_surcharge(show_manager, booking_manager)
    scenario_cancellation(show_manager, booking_manager)
    scenario_concurrency(show_manager)
    scenario_payment_failure(show_manager)


if __name__ == "__main__":
    main()
