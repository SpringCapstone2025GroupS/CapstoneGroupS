from dataclasses import dataclass
from typing import Any
import requests

from pydantic import ValidationError

from .exceptions import (
    NotamFetcherRequestError,
    NotamFetcherUnauthenticatedError,
    NotamFetcherUnexpectedError,
    NotamFetcherValidationError,
    NotamFetcherRateLimitError
)


from .api_schema import CoreNOTAMData, APIResponseSuccess, APIResponseError, APIResponseMessage 


class NotamRequest:
    page_num: int = 1
    page_size: int = 1000

@dataclass
class NotamLatLongRequest(NotamRequest):
    lat: float
    long: float
    radius: float

@dataclass
class NotamAirportCodeRequest(NotamRequest):
    airport_code: str

class NotamFetcher:
    FAA_API_URL = "https://external-api.faa.gov/notamapi/v1/notams"
    _page_size : int

    def __init__(self, client_id: str, client_secret: str, page_size: int = 1000):
        self.client_id = client_id
        self.client_secret = client_secret
        self.page_size=page_size

    @property
    def page_size(self):
        return self._page_size

    @page_size.setter
    def page_size(self, value: int):
        if value > 1000:
            raise ValueError("page_size should not exceed 1000")
        if value <= 0:
            raise ValueError("page_size must be greater than 0")
        self._page_size = value

    def fetch_notams_by_airport_code(self, airport_code: str):
        """
        Fetches ALL notams for a particular airport code.

        Args:
            airport_code (str): A valid ICAO airport code.

        Returns:
            List[CoreNOTAMData]: A complete list of NOTAMs for the airport code. An invalid airport code returns an empty list.
        
        Raises:
            NotamFetcherUnauthenticatedError: If NotamFetcher has invalid client id or secret.
            NotamFetcherRequestError: If a requests error occurs while fetching from the API.
        """
        request = NotamAirportCodeRequest(airport_code)
        request.page_size = self.page_size

        return self._fetch_all_notams(request)

    def fetch_notams_by_latlong_list(self, coords: list[tuple[float, float]],  radius: float = 100.0):
        """
        Fetches ALL distinct notams for each (latitude, longitude) coordinate..

        Args:
            coords (list[(float, float)]): The coordinate list to fetch NOTAMs from.
            radius (float): The location radius criteria in nautical miles. (max:100)

        Returns:
            List[CoreNOTAMData]: A complete list of NOTAMs for the location.

        Raises:
            NotamFetcherUnauthenticatedError: If NotamFetcher has invalid client id or secret.
            NotamFetcherRequestError: If a requests error occurs while fetching from the API.
            ValueError: If the radius is less than or equal to 0 or greater than 100.
        """
        all_notams: list[CoreNOTAMData] = []
        seen_notams: set[str] = set()

        for lat, long in coords:
            coord_notams = self.fetch_notams_by_latlong(lat, long, radius)
            new_notams = [notam for notam in coord_notams if notam.notam.id not in seen_notams]
            all_notams.extend(new_notams)
            for notam in new_notams:
                seen_notams.add(notam.notam.id)
                
        return all_notams

    def fetch_notams_by_latlong(self, lat: float, long: float, radius: float = 100.0):
        """
        Fetches ALL notams for a particular latitude and longitude.

        Args:
            lat (float): The latitude to fetch NOTAMs from.
            long (float): The longitude to fetch NOTAMs from.
            radius (float): The location radius criteria in nautical miles. (max:100)

        Returns:
            List[CoreNOTAMData]: A complete list of NOTAMs for the location.

        Raises:
            NotamFetcherUnauthenticatedError: If NotamFetcher has invalid client id or secret.
            NotamFetcherRequestError: If a requests error occurs while fetching from the API.
            ValueError: If the radius is less than or equal to 0 or greater than 100.
        """
        if radius > 100:
            raise ValueError(f"Radius must be less than 100")
        if radius <= 0:
            raise ValueError(f"Radius must be greater than 0")

        request = NotamLatLongRequest(lat, long, radius)
        request.page_size = self.page_size

        return self._fetch_all_notams(request)

    def _fetch_all_notams(self, request: NotamAirportCodeRequest | NotamLatLongRequest) -> list[CoreNOTAMData]:
        """
        Fetches NOTAMs across all pages from the the API.
        
        Args:
            request (NotamAirportCodeRequest | NotamLatLongRequest): The airport or Lat/Long to pull all NOTAMs from. Page is ignored.

        Returns:
            list[CoreNOTAMData] if all requests returned a Success response.
        Raises:
            NotamFetcherUnauthenticatedError: If NotamFetcher has invalid client id or secret.
            NotamFetcherRequestError: If a requests error occurs while fetching from the API.
        """

        notamItems: list[CoreNOTAMData] = []

        first_page = self._fetch_notams(request)

        notamItems.extend([item.properties.coreNOTAMData for item in first_page.items])

        for i in range(2, first_page.total_pages + 1):
            request.page_num = i
            nextPage = self._fetch_notams(request)

            notamItems.extend([item.properties.coreNOTAMData for item in nextPage.items])

        return notamItems

    def _fetch_notams(self, request: NotamAirportCodeRequest | NotamLatLongRequest) -> APIResponseSuccess:
        """
        Fetches and validates a response from the API.

        Args:
            reqeust: NotamAirportCodeRequest | NotamLatLongRequest

        Returns:
            APIResponseSuccess: if the request returned a Success response.

        Raises:
            NotamFetcherRequestError: If a request error occurs while fetching from the API.
            NotamFetcherUnexpectedError: If the response an unexpected error.
            NotamFetcherUnauthenticatedError: If NotamFetcher has invalid client id or secret.
            NotamFetcherValidationError: If the response was not an Success, Error, or Message response.
            ValueError: If the request request page_num is less than 1.
        """

        data = self._fetch_notams_raw(request)

        # the response dict can be an unvalidated APIResponseSuccess, APIResponseError, or APIResponseMessage
        # We try to validate the response as each type.
        # If it cannot be validated, a NotamFetcherValidationError is thrown.

        # APIResponseSuccess case
        try:
            return APIResponseSuccess.model_validate(data)
        except ValidationError:
            pass

        # APIResponseError case
        try:
            error_response = APIResponseError.model_validate(data)
            if error_response.error == "Invalid client id or secret":
                raise NotamFetcherUnauthenticatedError("Invalid client id or secret")

            raise NotamFetcherUnexpectedError(f"Unexpected Error: {error_response.error}")

        except ValidationError:
            pass

        # APIResponseMessage case
        try:
            message_response = APIResponseMessage.model_validate(data)
            raise NotamFetcherUnexpectedError(f"Unexpected Message: {message_response.message}")
        except ValidationError:
            raise NotamFetcherValidationError(f"Could not validate response from API.", data)

    def _fetch_notams_raw(self, request: NotamAirportCodeRequest | NotamLatLongRequest) -> dict[str, Any]:
        """
        Returns the JSON response as dict from the NOTAMs API.
        
        Args:
            request (NotamAirportCodeRequest | NotamLatLongRequest): The airport or Lat/Long to pull all NOTAMs from.

        Returns:
            dict[str, Any]: If the requests was successful.
        
        Raises:
            NotamFetcherRequestError if a requests error occured.
            NotamFetcherUnexpectedError if the response was invalid JSON.
        """
        query_string = {}

        if request.page_num < 1:
            raise ValueError("page_num must be greater than 0")
        if request.page_size > 1000:
            raise ValueError("page_size should not exceed 1000")

        if isinstance(request, NotamLatLongRequest):
            if request.radius > 100:
                raise ValueError("radius must be less than 100")
            if request.radius <= 0:
                raise ValueError("radius must be greater than 0")

            query_string = {
                "locationLongitude": str(request.long),
                "locationLatitude": str(request.lat),
                "locationRadius": str(request.radius),
                "pageNum": str(request.page_num),
                "pageSize": str(request.page_size),
            }

        if isinstance(request, NotamAirportCodeRequest):
            query_string = {
                "icaoLocation": str(request.airport_code),
                "pageNum": str(request.page_num),
                "pageSize": str(request.page_size),
            }

        try:
            response = requests.get(
                self.FAA_API_URL,
                headers={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
                params=query_string,
            )

        except requests.exceptions.RequestException as e:
            raise NotamFetcherRequestError from e

        # Check for a rate limit response
        if response.status_code == 429:
        # Assuming you have imported NotamFetcherRateLimitError from your exceptions module
            raise NotamFetcherRateLimitError()        
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            raise NotamFetcherUnexpectedError(f"Response from API unexpectedly not JSON. Received text: {response.text}") from e
