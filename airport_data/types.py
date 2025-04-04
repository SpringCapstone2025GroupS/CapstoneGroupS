from dataclasses import dataclass
from typing import Tuple




@dataclass(frozen=True)
class Airport:
    name: str
    country: str
    IATA: str | None
    ICAO: str
    coordinates: Tuple[float, float]
    altitude: int
    tz_name: str | None


