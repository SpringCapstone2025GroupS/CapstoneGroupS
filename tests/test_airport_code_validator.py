import pytest
from airport_code_validator.airport_code_validator import AirportCodeValidator
from airport_data.airport_data import AirportData
from airport_data.types import Airport



@pytest.mark.parametrize("airport, expected", [
    (Airport(name='JOHN F KENNEDY INTL', country='US', iata='JFK', icao='KJFK', coordinates=(40.63980103, -73.77890015), elevation=13, state_name='New_York'), True), 
    (Airport(name='TED STEVENS ANCHORAGE INTL', country='United States', iata='ANC', icao='PANC', coordinates=(61.17440032958984, -149.99600219726562), elevation=152, state_name='Alaska'), False), #Alaska
    (Airport(name='DANIEL K INOUYE INTL', country='United States', iata='HNL', icao='PHNL', coordinates=(21.32062, -157.924228), elevation=13, state_name='Hawaii'), False), # Hawaii
    (Airport(name='RAFAEL HERNANDEZ', country='Puerto Rico', iata='BQN', icao='TJBQ', coordinates=(18.49485222, -67.12944166), elevation=237.7, state_name=None), False), # Puerto Rico
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