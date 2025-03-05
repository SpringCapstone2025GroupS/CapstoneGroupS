from datetime import datetime
from typing import List, Optional
from datetime import datetime
from typing import List, Optional
from rich.console import Console

from notam_fetcher.api_schema import Notam



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
            f"Coordinates: {notam.coordinates}\n"
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

