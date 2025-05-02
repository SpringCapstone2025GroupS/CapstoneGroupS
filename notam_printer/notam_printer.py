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

    max_lines = None
    print_all_fields = False

    def __init__(self, max_lines: None|int=None, print_all_fields=False):
        if max_lines is not None and int(max_lines) <= 0:
            raise ValueError("max_lines must be a postive, non-zero integer")
        self.max_lines = max_lines
        self.print_all_fields = print_all_fields

    def print_notam(self, notam: Notam) -> str:
        if self.print_all_fields:
            return self.print_all_notam_fields(notam)
        elif self.max_lines:
            return self.print_notam_text(notam, self.max_lines)
        else:
            return self.print_notam_text(notam)

    def print_notam_text(self, notam: Notam, max_lines: None|int =None) -> str:
        if max_lines:
            return '\n'.join(notam.text.split('\n')[:max_lines]) + ('\n...' if len(notam.text.split('\n')) > max_lines else "" )
        else:
            return notam.text

    def print_separator(self):
        return "-"*80

    def print_all_notam_fields(self, notam: Notam) -> str:
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
            f"Text: {notam.text}"
        )

    def print_notams(self, notams: List[Notam]):

        """
        Takes a list of Notams and prints them in a legible format

        Args:
            notams (List[Notam]): A list of NOTAMs to be printed
        """

        console = Console()
        for notam in notams:
            console.print(self.print_notam(notam))
            console.print(self.print_separator())

    # print in NOTAM in FAA format
    def print_normal_format(self, notam: Notam) -> str:
        """
        Prints the NOTAM in FAA domestic format like:
        OKC 12/060 KOKC RWY 17R PAPI U/S 202501061400-202505102355
        """
        start_dt = notam.effective_start
        end_dt = notam.effective_end

        return (
            f"{notam.location} {notam.number} {notam.icao_location} "
            f"{self._get_affected_area(notam)} {self._get_status(notam)} "
            f"{start_dt.strftime('%Y%m%d%H%M')}-{end_dt.strftime('%Y%m%d%H%M')}"
        )

    def _get_affected_area(self, notam: Notam) -> str:
        """
        Tries to extract affected area like 'RWY 17R' from the text field.
        """
        for i, word in enumerate(notam.text.split()):
            if word == "RWY" and i + 1 < len(notam.text.split()):
                return f"RWY {notam.text.split()[i + 1]}"
        return "RWY UNKNOWN"

    def _get_status(self, notam: Notam) -> str:
        """
        Tries to detect status like 'U/S' (Unserviceable) or 'CLSD' (Closed).
        """
        if "U/S" in notam.text:
            return "U/S"
        elif "CLSD" in notam.text:
            return "CLSD"
        return "STATUS_UNKNOWN"