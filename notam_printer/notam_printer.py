from datetime import datetime
from typing import List, Optional
from rich.console import Console

# Define NotAM class
class Notam:

    id: str
    number: str
    type: str
    issued: str
    selection_code: Optional[str]
    location: str
    effective_start: str
    effective_end: str
    text: str
    maximumFL: Optional[str] = None
    classification: str
    account_id: str
    last_updated: datetime
    icao_location: str

    def __init__(
        self,
        id: str,
        number: str,
        type: str,
        issued: str,
        selection_code: Optional[str],
        location: str,
        effective_start: str,
        effective_end: str,
        text: str,
        maximumFL: Optional[str],
        classification: str,
        account_id: str,
        last_updated: str,
        icao_location: str,
    ):
        """ 
        Creates a NOTAM object with all necessary attributes
        Date strings are parsed into datetime objects for streamlined processing and organization 
        """
        self.id = id
        self.number = number
        self.type = type
        self.issued = issued
        self.selection_code = selection_code
        self.location = location
        self.effective_start = effective_start
        self.effective_end = effective_end
        self.text = text
        self.maximumFL = maximumFL
        self.classification = classification
        self.account_id = account_id
        self.last_updated = datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.icao_location = icao_location

class NotamPrinter:
    def formatNotam(self, notam: Notam) -> str:
        """
        Formats a Notam object into a legible string representation.

        Args:
            notam (Notam): The Notam object to format
        
        Returns:
            str: A formatted string representation of the Notam object
        """

        # Handling effective_end since it can be a string as well as a datetime object

        return (
            f"ID: {notam.id}\n"
            f"Number: {notam.number}\n"
            f"Type: {notam.type}\n"
            f"Issued: {notam.issued}\n"
            f"Selection Code: {notam.selection_code}\n"
            f"Location: {notam.location}\n"
            f"Effective Start: {notam.effective_start}\n"
            f"Effective End: {notam.effective_end}\n"
            f"Classification: {notam.classification}\n"
            f"Account ID: {notam.account_id}\n"
            f"Last Updated: {notam.last_updated}\n"
            f"ICAO Location: {notam.icao_location}\n"
            f"Text: {notam.text}\n"
            f"{'-' * 40}"
        )

    def print_notams(self, notams: List[Notam]):

        """
        Takes a list of Notams and prints them in a legible format

        Args:
            notams (List[Notam]): A list of NOTAMs to be printed
        """

        console = Console()
        for notam in notams:
            console.print(self.formatNotam(notam))
            console.print()
            console.print("-" * 80)
            console.print()
            