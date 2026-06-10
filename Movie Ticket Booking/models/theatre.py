from dataclasses import dataclass, field
from constants import City


@dataclass
class Theatre:
    id: str
    name: str
    city: City
    address: str

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Theatre) and self.id == other.id

    def __repr__(self):
        return f"Theatre({self.name}, {self.city.value})"
