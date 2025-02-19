from typing import Any
class NotamFetcherBaseError(Exception):
    """Base exception for NotamFetcher errors."""

class NotamFetcherUnexpectedError(NotamFetcherBaseError):
    """Raised when an unexpected error occurs"""

class NotamFetcherRequestError(NotamFetcherBaseError):
    """Raised when NotamFetcher receives a request exception while fetching from the API"""

class NotamFetcherUnauthenticatedError(NotamFetcherBaseError):
    """Raised when cliend_id or client_secret are invalid"""


class NotamFetcherValidationError(NotamFetcherBaseError):
    """Raised when Pydantic could not validate the response of the API"""
    invalid_object : Any
    def __init__(self, message: str, obj: Any):
        super().__init__(message)
        self.invalid_object = obj
