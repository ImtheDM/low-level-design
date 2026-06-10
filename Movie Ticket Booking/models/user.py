from dataclasses import dataclass
from constants import City


@dataclass
class User:
    id: str
    name: str
    email: str
    city: City

    def __repr__(self):
        return f"User({self.name}, {self.city.value})"
