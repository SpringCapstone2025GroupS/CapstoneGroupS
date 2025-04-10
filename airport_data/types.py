from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Airport:
    name: str
    country: str
    iata: str | None
    icao: str
    coordinates: Tuple[float, float]
    elevation: int
    tz_name: str | None
