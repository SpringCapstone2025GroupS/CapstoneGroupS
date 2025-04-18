from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class AirportBase:
    name: str
    country: str
    iata: str
    icao: str | None
    coordinates: Tuple[float, float]
    elevation: int
    state_name: str | None
