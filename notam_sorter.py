from typing import List

from notam_fetcher.api_schema import Notam



# Sorting class
class NotamSorter:
    def __init__(self, notams: List[Notam]):
        # Initialize the sorter with a list of NOTAM objects


        seen: set[str] = set()
        unique_notams: List[Notam] = []

        for notam in notams:
            if notam.id not in seen:
                seen.add(notam.id)
                unique_notams.append(notam)

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

