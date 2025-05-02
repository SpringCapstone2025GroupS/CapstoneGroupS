# type: ignore
import datetime
from typing import List, Optional
from dataclasses import dataclass
from geopy.distance import geodesic
from notam_fetcher.api_schema import Notam, Coordinate
from sorting_algorithm.sorting_algorithm import score

# Helpter: Before filtering, extract coordinates from Notam String
def parse_coords(coord_str: Optional[str]) -> Optional[tuple[float, float]]:
    if not coord_str:
        return None
    try:
        lat_str, lon_str = coord_str.strip().split()
        return float(lat_str), float(lon_str)
    except ValueError:
        print('Wrongly formatted coordinates.')
        return None
    
# Helper for flight phase
def parse_flight_level(fl: Optional[str]) -> Optional[int]:
    try:
        return int(fl) if fl else None
    except ValueError:
        print('Invalid Input')
        return None

# Filter 1 - Proximity
def filter_by_proximity (notams: List[Notam], ref_lat: float, ref_lon: float, max_distance_nm: float) -> List[Notam]:
    return [
        n for n in notams
        if geodesic((ref_lat, ref_lon), (n.lat, n.lon)).nautical < max_distance_nm # TODO: replace n.lat and n.lon with actual lat/lon values of Notams.
    ]

# Filter 2 - Flight Phase
def filter_by_flight_phase(notams: List[Notam], phase: str) -> List[Notam]
    def in_phase(n: Notam):
        min_fl = parse_flight_level(n.minimumFL)
        max_fl = parse_flight_level(n.maximumFL)
        if phase == "climb":
            return max_fl is not None and max_fl < 180
        elif phase == "cruise":
            return min_fl is not None and min_fl >= 180
        elif phase == "descent":
            return min_fl is not None and min_fl < 180
        return True
    return [n for n in notams if in_phase(n)]

# Filter 3: Severity (using already-implemented sorting)
def filter_by_severity(notams: List[Notam], severity) -> List[Notam]:
    return [n for n in notams if score(n) >= severity] 

# Filter 4: Time Window
def filter_by_time(notams: List[Notam], start: datetime.datetime, end: datetime.datetime) -> List[Notam]:
    return [
        n for n in notams
        if n.effective_start <= end and (
            isinstance(n.effective_end, datetime.datetime) and n.effective_end >= start
        )
    ]

# Filter 5: Notam Type
def filter_by_type(notams: List[Notam], types: List[str]) -> List[Notam]:
    return [n for n in notams if str(n.type).upper() in [t.upper() for t in types]]
