import pytest

import sys
import os

# Add the project root directory (parent of 'tests') to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import AirportData
from airport_data.airport_data import AirportData

@pytest.mark.parametrize("airport_code, expected_type", [
    ("JFK", tuple),  # Replace "JFK" with a valid IATA/ICAO code
    ("LAX", tuple),
    ("ORD", tuple),
    ("ZZZ", type(None)),  # An invalid airport code should return None
])
def test_get_airport_latlong(airport_code: str, expected_type: type):
    """Test retrieving latitude and longitude for known and unknown airports."""
    result = AirportData.get_airport_latlong(airport_code)
    assert isinstance(result, expected_type), f"Expected {expected_type}, got {type(result)}"

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", str),
    ("LAX", str),
    ("ORD", str),
    ("ZZZ", type(None)),  # Invalid code should return None
])
def test_get_airport_country(airport_code: str, expected: str):
    """Test retrieving the country of an airport."""
    result = AirportData.get_airport_country(airport_code)
    assert isinstance(result, expected), f"Expected {expected}, got {type(result)}"

@pytest.mark.parametrize("airport_code, expected", [
    ("JFK", str),
    ("LAX", str),
    ("ORD", str),
    ("ZZZ", type(None)),  # Invalid code should return None
])
def test_get_airport_timezone(airport_code: str, expected: str):
    """Test retrieving the timezone of an airport."""
    result = AirportData.get_airport_timezone(airport_code)
    assert isinstance(result, expected), f"Expected {expected}, got {type(result)}"
