import pytest
from airport_code_validator.airport_code_validator import AirportCodeValidator
from airport_data.airport_data import AirportData
from airport_data.types import Airport



@pytest.mark.parametrize("airport, expected", [
    (Airport(name='John F Kennedy International Airport', country='United States', iata='JFK', icao='KJFK', coordinates=(40.63980103, -73.77890015), elevation=13, tz_name='America/New_York'), True), 
    (Airport(name='Ted Stevens Anchorage International Airport', country='United States', iata='ANC', icao='PANC', coordinates=(61.17440032958984, -149.99600219726562), elevation=152, tz_name='America/Anchorage'), False),
    (Airport(name='Daniel K Inouye International Airport', country='United States', iata='HNL', icao='PHNL', coordinates=(21.32062, -157.924228), elevation=13, tz_name='Pacific/Honolulu'), False), # Hawaii
    (Airport(name='Lester B. Pearson International Airport', country='Canada', iata='YYZ', icao='CYYZ', coordinates=(43.6772003174, -79.63059997559999), elevation=569, tz_name='America/Toronto'), False),
])

def test_airports(airport: Airport, expected: bool):
    assert AirportCodeValidator.is_valid(airport) == expected


@pytest.mark.parametrize("code, expected", [
    ("JFK", True), ("KJFK", True),   # Valid US
    ("ANC", False), ("PANC", False), # Alaska
    ("HNL", False), ("PHNL", False), # Hawaii
    ("YYZ", False), ("CYYZ", False), # Non-US
])
def test_airports_from_code(code: str, expected: bool):
    airport = AirportData.get_airport(code)
    assert AirportCodeValidator.is_valid(airport) == expected