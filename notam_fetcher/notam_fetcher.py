import requests

from pydantic import ValidationError

from .exceptions import (
    NotamFetcherRequestError,
    NotamFetcherUnauthenticatedError,
    NotamFetcherUnexpectedError,
    NotamFetcherValidationError,
)


from .api_schema import Notam, NotamAPIResponse, NotamApiItem 



class NotamFetcher:
    FAA_API_URL = "https://external-api.faa.gov/notamapi/v1/notams"

    def __init__(self, client_id: str, client_secret: str, page_size: int = 1000):
        self.client_id = client_id
        self.client_secret = client_secret
        self._page_size = page_size

    def fetch_notams_by_airport_code(self, airport_code: str):
        """
        Fetches ALL notams for a particular latitude and longitude.

        Args:
            airport_code (str): A valid airport code.

        Raises:
            NotamFetcherRequestError: If a request error occurs while fetching from the API.
            NotamFetcherUnexpectedError: If an unexpected error occurs.
        Returns:
            Notams (List[Notam]): A list of NOTAMs
        """
        notamItems: list[Notam] = []

        first_page = self._fetch_notams_by_airport_code(airport_code, 1, self._page_size)

        notamItems.extend(
            [
                item.properties.coreNOTAMData.notam
                for item in first_page.items
                if isinstance(item, NotamApiItem)
            ]
        )

        for i in range(2, first_page.total_pages + 1):
            nextPage = self._fetch_notams_by_airport_code(airport_code, i, self._page_size)
            notamItems.extend(
                [
                    item.properties.coreNOTAMData.notam
                    for item in nextPage.items
                    if isinstance(item, NotamApiItem)
                ]
            )
        return notamItems

    def fetch_notams_by_latlong(self, lat: float, long: float, radius: float = 100.0):
        """
        Fetches ALL notams for a particular latitude and longitude.

        Args:
            lat (float): The latitude to fetch NOTAMs from
            long (float): The longitude to fetch NOTAMs from
            radius (float): The location radius criteria in nautical miles. (max:100)

        Raises:
            NotamFetcherRequestError: If a request error occurs while fetching from the API.
            NotamFetcherUnexpectedError: If an unexpected error occurs.
        Returns:
            Notams (List[Notam]): A list of NOTAMs
        """
        if radius > 100:
            raise ValueError(f"Radius must be less than 100")
        if radius <= 0:
            raise ValueError(f"Radius must be greater than 0")
        
        notamItems: list[Notam] = []

        first_page = self._fetch_notams_by_latlong(lat, long, radius, 1, self._page_size)

        notamItems.extend(
            [
                item.properties.coreNOTAMData.notam
                for item in first_page.items
                if isinstance(item, NotamApiItem)
            ]
        )

        for i in range(2, first_page.total_pages + 1):
            nextPage = self._fetch_notams_by_latlong(lat, long, radius, i, self._page_size)
            notamItems.extend(
                [
                    item.properties.coreNOTAMData.notam
                    for item in nextPage.items
                    if isinstance(item, NotamApiItem)
                ]
            )

        return notamItems

    def _fetch_notams_by_latlong(
        self, lat: float, long: float, radius: float, page_num: int, page_size: int = 1000
    ) -> NotamAPIResponse:
        """
        Fetches a response from the API using latitude and longitude.

        Args:
            lat (float): The latitude to fetch NOTAMs from
            long (float): The longitude to fetch NOTAMs from
            radius (float): The location radius criteria in nautical miles. (max:100)
            page_num (int): The page number of the response (min: 1)
            page_size (int): The number of NOTAMs per page (max: 1000)

        Returns:
            NotamAPIResponse: A Notam API Response

        Raises:
            NotamFetcherRequestError: If a request error occurs while fetching from the API.
            NotamFetcherUnexpectedError: If an unexpected error occurs.
        """
        if radius > 100:
            raise ValueError("radius must be less than 100")
        if radius <= 0:
            raise ValueError("radius must be greater than 0")
        if page_size > 1000:
            raise ValueError("page_size must be less than 1000")
        if page_num < 1:
            raise ValueError("page_num must be greater than 0")
        

        query_string = {
            "locationLongitude": str(long),
            "locationLatitude": str(lat),
            "locationRadius": str(radius),
            "page_num": str(page_num),
            "page_size": str(page_size),
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
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise (
                NotamFetcherUnexpectedError(
                    f"Response from API unexpectedly not JSON. Received text: {response.text} "
                )
            )
        if data.get("error", "") == "Invalid client id or secret":
            raise (NotamFetcherUnauthenticatedError("Invalid client id or secret"))
        try:
            valid_response = NotamAPIResponse.model_validate(data)
            return valid_response
        except ValidationError:
            raise (
                NotamFetcherValidationError(
                    f"Could not validate response from API.", data
                )
            )

    def _fetch_notams_by_airport_code(
        self, airport_code: str, page_num: int, page_size: int = 1000
    ) -> NotamAPIResponse:
        """
        Fetches a response from the API using latitude and longitude.

        Args:
            airport_code (str): A valid airport code.
            page_num (int): The page number of the response (min: 1)
            page_size (int): The number of NOTAMs per page (max: 1000)

        Returns:
            NotamAPIResponse: A Notam API Response

        Raises:
            NotamFetcherRequestError: If a request error occurs while fetching from the API.
            NotamFetcherUnexpectedError: If an unexpected error occurs.
        """
        if page_size > 1000:
            raise ValueError("page_size must be less than 1000")
        if page_num < 1:
            raise ValueError("page_num must be greater than 0")
        
        query_string = {
            "domesticLocation": str(airport_code),
            "page_num": str(page_num),
            "page_size": str(page_size),
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
            data = response.json()
        except requests.exceptions.JSONDecodeError:
            raise (
                NotamFetcherUnexpectedError(
                    f"Response from API unexpectedly not JSON. Received text: {response.text} "
                )
            )
        if data.get("error", "") == "Invalid client id or secret":
            raise (NotamFetcherUnauthenticatedError("Invalid client id or secret"))
        try:
            valid_response = NotamAPIResponse.model_validate(data)
            return valid_response
        except ValidationError:
            raise (
                NotamFetcherValidationError(
                    f"Could not validate response from API.",
                    data
                )
            )