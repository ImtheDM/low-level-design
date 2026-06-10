from dataclasses import dataclass, field


@dataclass
class Movie:
    id: str
    title: str
    duration_mins: int
    genre: str
    language: str

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Movie) and self.id == other.id

    def __repr__(self):
        return f"Movie({self.title}, {self.language}, {self.duration_mins}min)"
