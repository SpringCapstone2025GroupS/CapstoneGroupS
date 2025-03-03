from dataclasses import dataclass
from typing import Any
import requests

from pydantic import ValidationError

from .exceptions import (
    NotamFetcherRequestError,
    NotamFetcherUnauthenticatedError,
    NotamFetcherUnexpectedError,
    NotamFetcherValidationError,
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

    def __init__(self, client_id: str, client_secret: str, page_size: int = 1000):
        self.client_id = client_id
        self.client_secret = client_secret

        if page_size > 1000:
            raise ValueError("page_size must be less than 1000")
    
        self._page_size = page_size

    
    def fetch_notams_by_airport_code(self, airport_code: str):
        """
        Fetches ALL notams for a particular airport code.

        Args:
            airport_code (str): A valid ICAO airport code.

        Returns:
            List[CoreNOTAMData]: A complete list of NOTAMs for the airport code.
        
        Raises:
            NotamFetcherUnauthenticatedError: If NotamFetcher has invalid client id or secret.
            NotamFetcherRequestError: If a requests error occurs while fetching from the API.
        """
        request = NotamAirportCodeRequest(airport_code)
        request.page_size = self._page_size

        return self._fetch_all_notams(request)

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
        request.page_size = self._page_size

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
        if not isinstance(first_page, APIResponseSuccess):
            # Did not get a successful response while fetching one of the NOTAMs. Raise
            raise NotamFetcherUnexpectedError(first_page)

        first_page.total_pages
        notamItems.extend(
            [
                item.properties.coreNOTAMData
                for item in first_page.items
            ]
        )

        for i in range(2, first_page.total_pages + 1):
            request.page_num = i
            nextPage = self._fetch_notams(request)
            if not isinstance(nextPage, APIResponseSuccess):
                raise NotamFetcherUnexpectedError(nextPage)
            
            notamItems.extend(
                [
                    item.properties.coreNOTAMData
                    for item in nextPage.items
                ]
            )
        
        return notamItems
        
    def _fetch_notams(self, request: NotamAirportCodeRequest | NotamLatLongRequest) -> APIResponseSuccess | APIResponseError | APIResponseMessage:
        """
        Fetches and validates a response from the API.

        Args:
            reqeust: NotamAirportCodeRequest | NotamLatLongRequest

        Returns:
            APIResponseSuccess: if the request returned a Success response.
            APIResponseMessage: if the request returned a Message response.
            APIResponseError: if the request returned an Error response.

        Raises:
            NotamFetcherRequestError: If a request error occurs while fetching from the API.
            NotamFetcherUnexpectedError: If an unexpected error occurs.
            NotamFetcherUnauthenticatedError: If NotamFetcher has invalid client id or secret.
            NotamFetcherValidationError: If the response was not an Success, Error, or Message response.
            ValueError: If the request request page_num is less than 1.
        """
        if request.page_num < 1:
            raise ValueError("page_num must be greater than 0")

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
            raise NotamFetcherUnexpectedError(f"Unexpected message: {message_response.message}")
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
        query_string ={}

        if isinstance(request, NotamLatLongRequest):
            if request.radius > 100:
                raise ValueError("radius must be less than 100")
            if request.radius <= 0:
                raise ValueError("radius must be greater than 0")

            query_string = {
                "locationLongitude": str(request.long),
                "locationLatitude": str(request.lat),
                "locationRadius": str(request.radius),
                "page_num": str(request.page_num),
                "page_size": str(request.page_size),
            }

        if isinstance(request, NotamAirportCodeRequest):
            query_string = {
                "icaoLocation": str(request.airport_code),
                "page_num": str(request.page_num),
                "page_size": str(request.page_size),
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

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            raise (
                NotamFetcherUnexpectedError(
                    f"Response from API unexpectedly not JSON. Received text: {response.text} "
                )
            )
        
