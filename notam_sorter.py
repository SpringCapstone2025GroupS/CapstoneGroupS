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

    def get_max_flight_level(self) -> int:
        """Convert maximumFL to an integer if it's valid, otherwise return 0."""
        return int(self.maximumFL) if isinstance(self.maximumFL, str) and self.maximumFL.isdigit() else 0


# Sorting class
class NotamSorter:
    def __init__(self, notams: List[Notam]):
        # Initialize the sorter with a list of NOTAM objects
        self.notams: List[Notam] = notams

    def sort(self) -> List[Notam]:
        """
        Sort NOTAMs based on priority:
        1. Runway (RWY) and Taxiway (TWY) NOTAMs first
        2. Earlier start times come first
        3. Higher maximum flight level is prioritized if start times are the same
        4. If still equal, sort by NOTAM number
        """
        def sorting_key(notam: Notam):
            # Assigning priority to keywords (RWY higher than TWY)
            keyword_priority = (
                -1 if notam.selection_code == "RWY" else
                0 if notam.selection_code == "TWY" else
                1
            )

            # Convert maximum flight level (altitude) into an integer for comparison
            max_flight_level = notam.get_max_flight_level()

            # Extract numeric part of NOTAM number for tie-breaking
            notam_number = int("".join(filter(str.isdigit, notam.number))) if notam.number else 0

            # Sorting order:
            # - Higher priority (lower numerical value) comes first
            # - Earlier start times come first
            # - Higher max flight levels take priority if start times are the same
            # - If all else is equal, sort by NOTAM number
            return (keyword_priority, notam.effective_start.timestamp(), -max_flight_level, notam_number)


        sorted_list = sorted(self.notams, key=sorting_key)
        print([notam.number for notam in sorted_list])  # Debugging line
        return sorted_list
