import sys
import os

# Add the root directory of the project to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from notam_fetcher.exceptions import NotamFetcherRateLimitError
from notam_fetcher.notam_fetcher import NotamFetcher
import pytest
from typing import Any, Literal, Optional, Union, List, Dict


class MockRateLimitResponse:
    """Mocks a requests response that returns a 429 status code"""

    def __init__(self):
        self.status_code = 429  # forces the request status to be 429!

    def json(self) -> Dict[str, Any]:
        return {"error": "Rate limit exceeded"}


@pytest.fixture
def mock_rate_limit_response(monkeypatch):
    """Fixture to mock the API returning a 429 status code"""

    def returnRateLimit(*args: Any, **kwargs: Any) -> MockRateLimitResponse:
        return MockRateLimitResponse()

    monkeypatch.setattr("requests.get", returnRateLimit)


def test_fetch_notams_by_airport_code_rate_limit(mock_rate_limit_response):
    """Test that a rate limit error (429) correctly raises NotamFetcherRateLimitError
        When called on fetch_notam_by_airport_code"""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")

    with pytest.raises(NotamFetcherRateLimitError):
        notam_fetcher.fetch_notams_by_airport_code("JFK")


def test_fetch_notams_by_latlong_rate_limit(mock_rate_limit_response):
    """Test that a rate limit error (429) correctly raises NotamFetcherRateLimitError
        When called on fetch_notams_by_latlong"""
    notam_fetcher = NotamFetcher("CLIENT_ID", "CLIENT_SECRET")

    with pytest.raises(NotamFetcherRateLimitError):
        notam_fetcher.fetch_notams_by_latlong(32.0, -97.0, 50.0)
