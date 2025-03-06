from typing import Any

class AirportNotFoundError(Exception):
    """Raise when the Airport Code is not found in the dataset"""

class GapIsNotValid(Exception):
    """Raise when the gap provided is a invalid number"""