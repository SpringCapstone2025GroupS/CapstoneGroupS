import pytest

import sys
import os

from airport_data.types import Airport

# Add the project root directory (parent of 'tests') to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import AirportData
from airport_data.airport_data import AirportData

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", (40.63992805, -73.77869222)),
    ("KJFK", (40.63992805, -73.77869222)),
    ("LAX", (33.94249638, -118.40804861)),
    ("ORD", (41.97694027, -87.90814972)),
    ("JKA", (30.28963888, -87.67177777)),
    ("BHM", (33.56388888, -86.75230555)),
    ("GAD", (33.97264886, -86.08908344)),
    ("EET", (33.17777777, -86.78322222)),
    ("8A0", (34.22911111, -86.25575)),
])
def test_get_airport_latlong(airport_code: str, expected: tuple[float, float]):
    """Test retrieving latitude and longitude for known and unknown airports."""
    result = AirportData.get_airport_latlong(airport_code)
    assert result == expected

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", "US"),
    ("KJFK", "US"),
    ("LAX", "US"),
    ("ORD", "US"),
    ("MBSC", "TC"),
    ("JKA", "US"),
    ("BHM", "US"),
    ("GAD", "US"),
    ("EET", "US"),
    ("8A0", "US"),
])
def test_get_airport_country(airport_code: str, expected: str):
    """Test retrieving the country of an airport."""
    result = AirportData.get_airport_country(airport_code)
    assert result == expected

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", "NEW YORK"),
    ("KJFK", "NEW YORK"),
    ("LAX", "CALIFORNIA"),
    ("ORD", "ILLINOIS"),
    ("MBSC", None),  # Adjusted to handle NaN properly
    ("JKA", "ALABAMA"),
    ("BHM", "ALABAMA"),
    ("GAD", "ALABAMA"),
])
def test_get_airport_tz_name(airport_code: str, expected: str):
    """Test retrieving the state name of an airport."""
    result = AirportData.get_airport_state_name(airport_code)
    assert (result is None and expected is None) or result == expected

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", "JFK"),
    ("KJFK", "JFK"),
    ("MBSC", "MBSC"),
    ("JKA", "JKA"),
    ("BHM", "BHM"),
    ("GAD", "GAD"),
])

def test_get_airport_IATA(airport_code: str, expected: str):
    """Test retrieving the IATA of an airport."""
    result = AirportData.get_airport_iata(airport_code)
    assert result == expected

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", "KJFK"),
    ("KJFK", "KJFK"),
    ("MBSC", "MBSC"),
    ("JKA", "KJKA"),
    ("BHM", "KBHM"),
    ("GAD", "KGAD"),
    ("EET", "KEET"),
    ("8A0", None),
])
def test_get_airport_ICAO(airport_code: str, expected: str):
    """Test retrieving the ICAO of an airport."""
    result = AirportData.get_airport_icao(airport_code)
    assert result == expected

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", 13),
    ("MBSC", 9),
    ("JKA", 17),
    ("BHM", 650),
    ("GAD", 569),
    ("EET", 585),
    ("8A0", 1032),
])
def test_get_airport_altitude(airport_code: str, expected: int):
    """Test retrieving the altitude of an airport."""
    result = AirportData.get_airport_elevation(airport_code)
    assert result == expected

def test_get_airport():
    jfk_expected = Airport(
        name="JOHN F KENNEDY INTL",
        country="US",
        iata="JFK",
        icao="KJFK",
        coordinates=(40.63992805, -73.77869222),
        elevation=13,
        state_name="NEW YORK",
    )

    jfk_airport = AirportData.get_airport('JFK')
    assert jfk_airport == jfk_expected

    jka_expected = Airport(
        name="GULF SHORES INTL/JACK EDWARDS FLD",
        country="US",
        iata="JKA",
        icao="KJKA",
        coordinates=(30.28963888, -87.67177777),
        elevation=17,
        state_name="ALABAMA",
    )

    jka_airport = AirportData.get_airport('JKA')
    assert jka_airport == jka_expected

    with pytest.raises(ValueError):
        AirportData.get_airport('ZZZ')
