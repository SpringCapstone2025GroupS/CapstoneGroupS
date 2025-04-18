import pytest

import sys
import os

from airport_data.types import Airport

# Add the project root directory (parent of 'tests') to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import AirportData
from airport_data.airport_data import AirportData

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", (40.63980103, -73.77890015)),
    ("KJFK", (40.63980103, -73.77890015)),
    ("LAX", (33.94250107, -118.4079971) ),
    ("ORD", (41.9786, -87.9048)),
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
])
def test_get_airport_country(airport_code: str, expected: str):
    """Test retrieving the country of an airport."""
    result = AirportData.get_airport_country(airport_code)
    assert result == expected

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", "NEW YORK"),
    ("KJFK", "NEW YORK"),
    ("LAX", "CALIFORNIA"),
    ("ORD", "CHICAGO"),
    ("MBSC", None),  
])
def test_get_airport_tz_name(airport_code: str, expected: str):
    """Test retrieving the state name of an airport."""
    result = AirportData.get_airport_state_name(airport_code)
    assert result == expected

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", "JOHN F KENNEDY INTL"),
    ("KJFK", "JOHN F KENNEDY INTL"),
    ("MBSC", "SOUTH CAICOS INTL"),  
])
def test_get_airport_name(airport_code: str, expected: str):
    """Test retrieving the airport name of an airport."""
    result = AirportData.get_airport_name(airport_code)
    assert result == expected

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", "JFK"),
    ("KJFK", "JFK"),
    ("MBSC", None) 
])
def test_get_airport_IATA(airport_code: str, expected: str):
    """Test retrieving the IATA of an airport."""
    result = AirportData.get_airport_iata(airport_code)
    assert result == expected


@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", "KJFK"),
    ("KJFK", "KJFK"),
    ("MBSC", "MBSC"),  
])
def test_get_airport_ICAO(airport_code: str, expected: str):
    """Test retrieving the ICAO of an airport."""
    result = AirportData.get_airport_icao(airport_code)
    assert result == expected

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", 13),
    ("MBSC", 9),  
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
        coordinates=(40.63980103, -73.77890015),
        elevation=13,
        state_name="NEW YORK",
    )

    jfk_airport = AirportData.get_airport('JFK')
    assert jfk_airport == jfk_expected

    with pytest.raises(ValueError):
        AirportData.get_airport('ZZZ')
