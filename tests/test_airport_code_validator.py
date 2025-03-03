import pytest
from unittest.mock import patch
import pandas as pd
from airport_code_validator.airport_code_validator import AirportCodeValidator

@pytest.fixture
def mock_airports():
    """Fixture to mock pandas.read_csv"""
    mock_data = pd.DataFrame({
        "IATA": ["JFK", "ANC", "HNL", "YYZ"],
        "ICAO": ["KJFK", "PANC", "PHNL", "CYYZ"],
        "Country": ["United States", "United States", "United States", "Canada"],
        "Tz Database Timezone": ["America/New_York", "America/Anchorage", "Pacific/Honolulu", "America/Toronto"]
    })
    with patch("pandas.read_csv", return_value=mock_data):
        yield

@pytest.mark.parametrize("code, expected", [
    ("JFK", True), ("KJFK", True),   # Valid US
    ("ANC", False), ("PANC", False), # Alaska
    ("HNL", False), ("PHNL", False), # Hawaii
    ("YYZ", False), ("CYYZ", False), # Non-US
    ("FAKE", False)                  # Non-existent
])

def test_airports(mock_airports: None, code: str, expected: bool):
    assert AirportCodeValidator.is_valid(code) == expected