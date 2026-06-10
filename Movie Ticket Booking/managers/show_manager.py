from typing import List
from models.movie import Movie
from models.theatre import Theatre
from models.screen import Screen
from models.seat import Seat
from models.show import Show
from constants import City, SeatStatus


class ShowManager:
    """Registry for all shows. Entry point for city-level browsing."""

    def __init__(self):
        self._shows: List[Show] = []
        # screen_id -> list[Seat]  (static seat layout per screen)
        self._screen_seats: dict[str, List[Seat]] = {}

    def register_seats(self, screen: Screen, seats: List[Seat]):
        self._screen_seats[screen.id] = seats

    def register_show(self, show: Show):
        seats = self._screen_seats.get(show.screen.id, [])
        for seat in seats:
            show.seat_status[seat.id] = SeatStatus.AVAILABLE
        self._shows.append(show)

    # ── city-level browsing ──────────────────────────────────────────────────

    def get_movies_by_city(self, city: City) -> List[Movie]:
        seen = set()
        movies = []
        for show in self._shows:
            if show.screen.theatre.city == city and show.movie not in seen:
                seen.add(show.movie)
                movies.append(show.movie)
        return movies

    def get_theatres_by_city_and_movie(self, city: City, movie: Movie) -> List[Theatre]:
        seen = set()
        theatres = []
        for show in self._shows:
            theatre = show.screen.theatre
            if theatre.city == city and show.movie == movie and theatre not in seen:
                seen.add(theatre)
                theatres.append(theatre)
        return theatres

    def get_shows_by_theatre_and_movie(self, theatre: Theatre, movie: Movie) -> List[Show]:
        return [
            s for s in self._shows
            if s.screen.theatre == theatre and s.movie == movie
        ]

    def get_show_by_id(self, show_id: str) -> Show:
        for show in self._shows:
            if show.id == show_id:
                return show
        raise KeyError(f"Show {show_id} not found.")

    def get_seats_for_screen(self, screen_id: str) -> List[Seat]:
        return self._screen_seats.get(screen_id, [])
