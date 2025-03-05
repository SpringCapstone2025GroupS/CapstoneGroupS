from typing import List, Optional
from datetime import datetime

# Define NOTAM class
class Notam:
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
        self.effective_start = datetime.strptime(effective_start, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.effective_end = datetime.strptime(effective_end, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.text = text
        self.maximumFL = maximumFL
        self.classification = classification
        self.account_id = account_id
        self.last_updated = datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.icao_location = icao_location

# Sorting class
class NotamSorter:
    def __init__(self, notams: List[Notam]):
        # Initialize the sorter with a list of NOTAM objects
        self.notams: List[Notam] = notams

        """
        Sort NOTAMs based on priority:
        1. Runway (RWY) and Taxiway (TWY) NOTAMs first
        2. Earlier start times come first
        3. Higher maximum flight level is prioritized if start times are the same
        4. If still equal, sort by NOTAM number
        """

    def sort(self) -> List[Notam]:
        def sorting_key(notam: Notam):
            # Assigning priority to keywords
            keyword_priority = -1 if "RWY" in notam.text else -2 if "TWY" in notam.text else 0
            # Convert maximum flight level to integer
            max_flight_level = (
                int(notam.maximumFL) if isinstance(notam.maximumFL, str) and notam.maximumFL.isdigit() else 0
            )
            # Extract numeric part of NOTAM number for tie-breaking
            notam_number = int("".join(filter(str.isdigit, notam.number))) if notam.number else 0

            return (keyword_priority, notam.effective_start, -max_flight_level, notam_number)

        return sorted(self.notams, key=sorting_key)

# Test the sorting with mock data
if __name__ == "__main__":
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
        ),
    ]

    # Soting the NOTAMS
    sorter = NotamSorter(sample_notams)
    sorted_list = sorter.sort()

    # Print the sorted NOTAMs
    for notam in sorted_list:
        print(f"{notam.number} - {notam.text} - Start: {notam.effective_start} - Max FL: {notam.maximumFL}")
