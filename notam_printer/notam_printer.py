from datetime import datetime
from typing import List, Optional
from datetime import datetime
from typing import List, Optional
from rich.console import Console

# Define NotAM class
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
        Formats a NotAM object into a legible string representation.

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

# Test printing with mock data.
if __name__ == '__main__':
    sample_notams = [
        Notam(
            id="1",
            number="A150/24",
            type="N",
            issued="2024-02-24T10:00:00.000Z",
            selection_code="RWY",
            location="JFK",
            effective_start="2024-02-25T12:00:00.000Z",
            effective_end="2024-02-26T12:00:00.000Z",
            text="Runway maintenance",
            maximumFL="040",
            classification="INTL",
            account_id="JFK",
            last_updated="2024-02-24T11:00:00.000Z",
            icao_location="KJFK",
        ),
        Notam(
            id="2",
            number="A151/24",
            type="N",
            issued="2024-02-24T11:00:00.000Z",
            selection_code="GEN",
            location="LAX",
            effective_start="2024-02-25T14:00:00.000Z",
            effective_end="2024-02-27T14:00:00.000Z",
            text="General notice",
            maximumFL="030",
            classification="DOM",
            account_id="LAX",
            last_updated="2024-02-24T12:00:00.000Z",
            icao_location="KLAX",
        ),
        Notam(
            id="3",
            number="A149/24",
            type="N",
            issued="2024-02-24T09:00:00.000Z",
            selection_code="TWY",
            location="ORD",
            effective_start="2024-02-25T11:00:00.000Z",
            effective_end="2024-02-27T11:00:00.000Z",
            text="Taxiway closed",
            maximumFL="050",
            classification="INTL",
            account_id="ORD",
            last_updated="2024-02-24T10:30:00.000Z",
            icao_location="KORD",
        )
    ]

    printer = NotamPrinter()
    printer.print_notams(sample_notams)
