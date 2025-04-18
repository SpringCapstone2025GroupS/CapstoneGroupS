import pytest
import sys
import os
from airport_base_ais.types import AirportBase

# Add the project root directory (parent of 'tests') to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from airport_base_ais.airport_base_ais import AirportBaseAIS

# Define a fixture for the airport code
@pytest.fixture
def airport_code():
    return "JFK"

def test_get_airport_latlong_structure(airport_code):
    """Test that latitude and longitude are valid floats."""
    lat, long = AirportBaseAIS.get_airport_latlong(airport_code)
    assert isinstance(lat, float), "Latitude should be a float"
    assert isinstance(long, float), "Longitude should be a float"
    assert -90 <= lat <= 90, "Latitude should be within valid range (-90 to 90)"
    assert -180 <= long <= 180, "Longitude should be within valid range (-180 to 180)"

def test_get_airport_country_validity(airport_code):
    """Test that the country code is a valid string."""
    country = AirportBaseAIS.get_airport_country(airport_code)
    assert isinstance(country, str), "Country code should be a string"
    assert len(country) == 2, "Country code should be a 2-character ISO code"

def test_get_airport_elevation_validity(airport_code):
    """Test that the elevation is a valid integer."""
    elevation = AirportBaseAIS.get_airport_elevation(airport_code)
    assert isinstance(elevation, int), "Elevation should be an integer"
    assert elevation >= -500, "Elevation should not be below -500 meters"
    assert elevation <= 10000, "Elevation should not exceed 10,000 meters"

def test_get_airport_object_structure(airport_code):
    """Test that the Airport object has all required fields."""
    airport = AirportBaseAIS.get_airport(airport_code)
    assert isinstance(airport, AirportBase), "Result should be an Airport object"
    assert isinstance(airport.name, str), "Airport name should be a string"
    assert isinstance(airport.country, str), "Country should be a string"
    assert isinstance(airport.iata, str), "IATA code should be a string"
    assert isinstance(airport.icao, str), "ICAO code should be a string"
    assert isinstance(airport.coordinates, tuple), "Coordinates should be a tuple"
    assert len(airport.coordinates) == 2, "Coordinates should have two elements (lat, long)"
    assert isinstance(airport.elevation, int), "Elevation should be an integer"
    assert isinstance(airport.state_name, (str, type(None))), "State name should be a string or None"

def test_get_airport_handles_invalid_code():
    """Test that invalid airport codes raise appropriate errors."""
    invalid_code = "ZZZ"
    with pytest.raises(ValueError, match=f"Airport code '{invalid_code}' not found"):
        AirportBaseAIS.get_airport(invalid_code)

@pytest.mark.parametrize("airport_code", ["JFK", "LAX", "ORD", "MBSC", "JKA"])
def test_get_airport_generic_fields(airport_code):
    """Test that generic fields are non-empty for valid airport codes."""
    airport = AirportBaseAIS.get_airport(airport_code)
    assert airport.name, "Airport name should not be empty"
    assert airport.country, "Country code should not be empty"
    assert airport.iata, "IATA code should not be empty"
    assert airport.icao, "ICAO code should not be empty"
    assert airport.coordinates, "Coordinates should not be empty"
    assert airport.elevation is not None, "Elevation should not be None"

# Define expected data for JFK
jfk_expected = AirportBase(
    name="JOHN F KENNEDY INTL",
    country="US",
    iata="JFK",
    icao="KJFK",
    coordinates=(40.63992805, -73.77869222),
    elevation=13,
    state_name="NEW YORK",
)

def test_get_airport_jfk():
    """Test retrieving the JFK airport object."""
    jfk_airport = AirportBaseAIS.get_airport("JFK")
    assert jfk_airport == jfk_expected

# Define expected data for JKA
jka_expected = AirportBase(
    name="GULF SHORES INTL/JACK EDWARDS FLD",
    country="US",
    iata="JKA",
    icao="KJKA",
    coordinates=(30.28963888, -87.67177777),
    elevation=17,
    state_name="ALABAMA",
)

def test_get_airport_jka():
    """Test retrieving the JKA airport object."""
    jka_airport = AirportBaseAIS.get_airport("JKA")
    assert jka_airport == jka_expected

def test_get_airport_invalid_code():
    """Test retrieving an invalid airport code."""
    with pytest.raises(ValueError):
        AirportBaseAIS.get_airport("ZZZ")
