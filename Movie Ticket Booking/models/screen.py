from dataclasses import dataclass, field
from .theatre import Theatre


@dataclass
class Screen:
    id: str
    name: str
    theatre: Theatre
    total_rows: int
    total_cols: int

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Screen({self.name} @ {self.theatre.name})"
