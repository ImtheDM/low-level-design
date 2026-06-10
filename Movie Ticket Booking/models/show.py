from dataclasses import dataclass, field
from datetime import datetime
from .movie import Movie
from .screen import Screen
from .seat import Seat
from constants import SeatStatus


@dataclass
class Show:
    id: str
    movie: Movie
    screen: Screen
    start_time: datetime
    # seat_id -> SeatStatus (mutable, managed by SeatManager under a lock)
    seat_status: dict = field(default_factory=dict)

    def __post_init__(self):
        # initialized externally by SeatManager after seats are added to the screen
        pass

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Show({self.movie.title} @ {self.screen.name}, {self.start_time.strftime('%d-%b %I:%M%p')})"
