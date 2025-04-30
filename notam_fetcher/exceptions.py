from typing import Any
class NotamFetcherBaseError(Exception):
    """Base exception for NotamFetcher errors."""

class NotamFetcherUnexpectedError(NotamFetcherBaseError):
    """Raised when an unexpected error occurs"""

class NotamFetcherRequestError(NotamFetcherBaseError):
    """Raised when NotamFetcher receives a request exception while fetching from the API"""

class NotamFetcherUnauthenticatedError(NotamFetcherBaseError):
    """Raised when client_id or client_secret are invalid"""


class NotamFetcherValidationError(NotamFetcherBaseError):
    """Raised when Pydantic could not validate the response of the API"""
    invalid_object : Any
    def __init__(self, message: str, obj: Any):
        super().__init__(message)
        self.invalid_object = obj

class NotamFetcherRateLimitError(NotamFetcherBaseError):
    """The FAA API applies rate limiting on a rolling basis, meaning the limit (30 requests per minute) is not strictly measured from the time we send our first request.
        Instead, the API likely tracks requests based on its own internal clock, so you might sometimes be able to make more than 30 requests before hitting the limit."""

    def __init__(self):
        message = "Rate limit exceeded. Try again later."

class NotamFetcherTimeoutReached(NotamFetcherBaseError):
    """Raised when NotamFetcher is terminated early because it exceeded the timeout."""