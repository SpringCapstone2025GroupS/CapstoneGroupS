from pytest import MonkeyPatch
import pytest
import requests
from notam_fetcher.exceptions import NotamFetcherUnauthenticatedError, NotamFetcherUnexpectedError, NotamFetcherValidationError
from notam_fetcher.notam_fetcher import NotamFetcher

from typing import Any


class MockResponse:
    """
    This class only mocks the .json() of a request.Response.

    Used to test different JSON responses.

    Example:
    monkeypatch.setattr(requests, "get", returnInvalid)

    """
    def __init__(self, response: dict[str, Any]):
        self.response = response

    def json(self) -> dict[str, Any]:
        return self.response


@pytest.fixture
def mock_api_returns_response_error(monkeypatch: MonkeyPatch):
    def return_error(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(
            {"error": "Response returned an error"}
        )
    monkeypatch.setattr(requests, "get", return_error)

@pytest.fixture
def mock_api_returns_response_message(monkeypatch: MonkeyPatch):
    def return_message(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(
            {"message": "Response returned a message"}
        )
    monkeypatch.setattr(requests, "get", return_message)

@pytest.fixture
def mock_api_returns_invalid_json(monkeypatch: MonkeyPatch):
    def returnInvalid(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(
            {"Invalid": "This object does not match the schema and cannot be validated"}
        )

    monkeypatch.setattr(requests, "get", returnInvalid)



@pytest.fixture
def mock_unexpected_response(monkeypatch: MonkeyPatch):
    def returnUnexpected(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(
            {
                "pageSize": 10,
                "pageNum": 3,
                "totalCount": 124,
                "totalPages": 13,
                "items": [
                    {
                        "type": "Point",
                        "geometry": {"type": "Point", "coordinates": [0]},
                        "properties": {"name": "Dinagat Islands"},
                    }
                ],
            }
        )

    monkeypatch.setattr(requests, "get", returnUnexpected)



@pytest.fixture
def mock_unauthorized_response(monkeypatch: MonkeyPatch):
    def returnEmpty(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse({
            "error": "Invalid client id or secret"
        })

    monkeypatch.setattr(requests, "get", returnEmpty)

@pytest.fixture
def mock_valid_response(monkeypatch: MonkeyPatch):
    def returnEmpty(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(
            {
                "pageSize": 50,
                "pageNum": 1,
                "totalCount": 2,
                "totalPages": 1,
                "items": [
                    {
                        "type": "Feature",
                        "properties": {
                            "coreNOTAMData": {
                                "notamEvent": {"scenario": "6000"},
                                "notam": {
                                    "id": "NOTAM_1_73849637",
                                    "series": "A",
                                    "number": "A2157/24",
                                    "type": "N",
                                    "issued": "2024-10-02T19:54:00.000Z",
                                    "affectedFIR": "KZJX",
                                    "selectionCode": "QCBLS",
                                    "minimumFL": "000",
                                    "maximumFL": "040",
                                    "location": "ZJX",
                                    "effectiveStart": "2024-10-02T19:50:00.000Z",
                                    "effectiveEnd": "2024-10-14T22:00:00.000Z",
                                    "text": "ZJX AIRSPACE ADS-B, AUTO DEPENDENT SURVEILLANCE\nREBROADCAST (ADS-R), TFC INFO SER BCST (TIS-B), FLT INFO SER\nBCST (FIS-B) SER MAY NOT BE AVBL WI AN AREA DEFINED AS 49NM\nRADIUS OF 322403N0781209W.",
                                    "classification": "INTL",
                                    "accountId": "KZJX",
                                    "lastUpdated": "2024-10-02T19:54:00.000Z",
                                    "icaoLocation": "KZJX",
                                    "lowerLimit": "SFC",
                                    "upperLimit": "3999FT.",
                                },
                                "notamTranslation": [
                                    {
                                        "type": "ICAO",
                                        "formattedText": "A2157/24 NOTAMN\nQ) KZJX/QCBLS////000/040/\nA) KZJX\nB) 2410021950\nC) 2410142200 EST\nE) ZJX AIRSPACE ADS-B, AUTO DEPENDENT SURVEILLANCE\nREBROADCAST (ADS-R), TFC INFO SER BCST (TIS-B), FLT INFO SER\nBCST (FIS-B) SER MAY NOT BE AVBL WI AN AREA DEFINED AS 49NM\nRADIUS OF 322403N0781209W.\nF) SFC   G) 3999FT.",
                                    }
                                ],
                            }
                        },
                        "geometry": {"type": "GeometryCollection"},
                    }
                ],
            }
        )

    monkeypatch.setattr(requests, "get", returnEmpty)


@pytest.fixture
def mock_empty_response(monkeypatch: MonkeyPatch):
    def returnEmpty(*args: Any, **kwargs: Any) -> MockResponse:
        return MockResponse(
            {
                "pageSize": 50,
                "pageNum": 1,
                "totalCount": 0,
                "totalPages": 0,
                "items": [],
            }
        )

    monkeypatch.setattr(requests, "get", returnEmpty)


def test_fetch_notams_by_latlong_invalid_json(mock_api_returns_invalid_json: None):
    """Test that an invalid schema from the API raises validation error"""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")

    with pytest.raises(NotamFetcherValidationError) as e:
        notam_fetcher.fetch_notams_by_latlong(32, 32, 10)

    assert (
        e.value.invalid_object.get("Invalid")
        == "This object does not match the schema and cannot be validated"
    )



def test_fetch_notams_by_latlong_unexpected_response(mock_unexpected_response: None):
    """Test that fetch_notams_by_latlong filters a non-notam object in the NOTAMs API response"""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")
    with pytest.raises(NotamFetcherValidationError):
        notam_fetcher.fetch_notams_by_latlong(32, 32, 10)


def test_fetch_notams_by_latlong_no_notams(mock_empty_response: None):
    """Test that fetch_notams_by_latlong handles the case where API returns no NOTAMs"""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")
    notams = notam_fetcher.fetch_notams_by_latlong(32, 32, 10)
    assert len(notams) == 0


def test_fetch_notams_by_airport_code_no_notams(mock_empty_response: None):
    """Test that fetch_notams_by_airport_code handles the case where API returns no NOTAMs"""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")
    notams = notam_fetcher.fetch_notams_by_airport_code("LAX")
    assert len(notams) == 0


def test_fetch_notams_response_error(mock_api_returns_response_error: None):
    """Test that fetch_notams_by_airport_code raises NotamFetcherUnexpectedError when response returns an error."""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")
    with pytest.raises(NotamFetcherUnexpectedError) as e:
        notam_fetcher.fetch_notams_by_airport_code("LAX")
    assert(str(e.value) == "Unexpected Error: Response returned an error")

    with pytest.raises(NotamFetcherUnexpectedError) as e:
        notam_fetcher.fetch_notams_by_latlong(30, 30)
    assert(str(e.value) == "Unexpected Error: Response returned an error")

def test_fetch_notams_response_message(mock_api_returns_response_message: None):
    """Test that fetch_notams_by_airport_code raises NotamFetcherUnexpectedError when response returns a message."""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")
    with pytest.raises(NotamFetcherUnexpectedError) as e:
        notam_fetcher.fetch_notams_by_airport_code("LAX")
    assert(str(e.value) == "Unexpected Message: Response returned a message")

    with pytest.raises(NotamFetcherUnexpectedError) as e:
        notam_fetcher.fetch_notams_by_latlong(30, 30)
    assert(str(e.value) == "Unexpected Message: Response returned a message")

def test_fetch_notams_unauthorized(mock_unauthorized_response: None):
    """Test that fetch_notams_by_airport_code handles the case where API returns no NOTAMs"""
    notam_fetcher = NotamFetcher("INVALID_CLIENT_ID", "CLIENT_SECRET")
    with pytest.raises(NotamFetcherUnauthenticatedError):
        notam_fetcher.fetch_notams_by_airport_code("LAX")

    with pytest.raises(NotamFetcherUnauthenticatedError):
        notam_fetcher.fetch_notams_by_latlong(32, 32, 10)


def test_notam_fetcher_page_size_constraints():
    """
    Tests that only setting the page_size to an invalid size throws a ValueError.
    """
    with pytest.raises(ValueError):
        NotamFetcher("CLIENT_ID", "CLIENT_SECRET", page_size=10001)
    with pytest.raises(ValueError):
        NotamFetcher("CLIENT_ID", "CLIENT_SECRET", page_size=0)

    valid_client = NotamFetcher("CLIENT_ID", "CLIENT_SECRET", page_size=1000)
    assert(valid_client.page_size==1000)
    valid_client = NotamFetcher("CLIENT_ID", "CLIENT_SECRET", page_size=1)
    assert(valid_client.page_size==1)

    valid_client.page_size=10
    assert(valid_client.page_size==10)
    
    with pytest.raises(ValueError):
        valid_client.page_size=-1
    with pytest.raises(ValueError):
        valid_client.page_size=0
    with pytest.raises(ValueError):
        valid_client.page_size=1001
    

def test_request_params(monkeypatch: MonkeyPatch):
    """
    Tests that the parameters of outbound requests from NotamFetcher are set correctly. 
    """

    TEST_LAT = 35
    TEST_LONG = -105
    TEST_RADIUS = 100.0
    TEST_PAGE_SIZE = 500

    TEST_AIRPORT_CODE = 'DEN'
    
    def assert_lat_long_params_and_return_empty(*args: Any, **kwargs: Any) -> MockResponse:
        assert(kwargs.get('params') == 
            {
                "locationLongitude": str(TEST_LONG),
                "locationLatitude": str(TEST_LAT),
                "locationRadius": str(TEST_RADIUS),
                "pageNum": str(1),
                "pageSize": str(TEST_PAGE_SIZE),
            }
        )
        return MockResponse(
            {
                "pageSize": TEST_PAGE_SIZE,
                "pageNum": 1,
                "totalCount": 0,
                "totalPages": 0,
                "items": [],
            }
        )
    
    monkeypatch.setattr(requests, "get", assert_lat_long_params_and_return_empty)

    client = NotamFetcher("CLIENT_ID", "CLIENT_SCRET", page_size=TEST_PAGE_SIZE)
    client.fetch_notams_by_latlong(TEST_LAT, TEST_LONG)


    def assert_airport_code_params_and_return_empty(*args: Any, **kwargs: Any) -> MockResponse:
        assert(kwargs.get('params') == 
            {
                "icaoLocation": str(TEST_AIRPORT_CODE),
                "pageNum": str(1),
                "pageSize": str(TEST_PAGE_SIZE),
            }
        )
        return MockResponse(
            {
                "pageSize": TEST_PAGE_SIZE,
                "pageNum": 1,
                "totalCount": 0,
                "totalPages": 0,
                "items": [],
            }
        )
    monkeypatch.setattr(requests, "get", assert_airport_code_params_and_return_empty)
    client.fetch_notams_by_airport_code(TEST_AIRPORT_CODE)
    
    