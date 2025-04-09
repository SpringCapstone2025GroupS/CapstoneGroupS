from typing import Optional
from datetime import datetime, UTC

# Define NOTAM class
class Notam:
    def __init__(
        self,
        id: str,
        number: str,
        type: str,
        issued: datetime,
        selection_code: Optional[str],
        location: str,
        effective_start: datetime,
        effective_end: datetime,
        text: str,
        maximumFL: Optional[str],
        classification: str,
        account_id: str,
        last_updated: datetime,
        icao_location: str,
    ):
        """ 
        Creates a NOTAM object with all necessary attributes
        Date objects are used directly for streamlined processing
        """
        self.id = id
        self.number = number
        self.type = type
        self.issued = issued.replace(tzinfo=UTC)
        self.selection_code = selection_code
        self.location = location
        self.effective_start = effective_start.replace(tzinfo=UTC)
        self.effective_end = effective_end.replace(tzinfo=UTC)
        self.text = text
        self.maximumFL = maximumFL
        self.classification = classification
        self.account_id = account_id
        self.last_updated = last_updated.replace(tzinfo=UTC)
        self.icao_location = icao_location

        # Compute and store a score for sorting/filtering
        self.score = self.compute_score()

    def get_max_flight_level(self) -> int:
        """Convert maximumFL to an integer if it's valid, otherwise return 0."""
        return int(self.maximumFL) if isinstance(self.maximumFL, str) and self.maximumFL.isdigit() else 0

    def compute_score(self) -> float:
        """
        Score this NOTAM based on its duration, recency, and type.
        Adjust the weights to fit the use case.
        """
        score = 0.0

        score += self.score_duration()
        score += self.score_recency()
        score += self.score_type()

        return score
    
    # this can be changed or removed if not needed
    def score_duration(self) -> float:
        return (self.effective_end - self.effective_start).total_seconds() / 3600
    
    # this can be changed or removed if not needed
    def score_recency(self) -> float:
        now = datetime.now(UTC)
        age_hours = (now - self.issued).total_seconds() / 3600
        return max(0, 24 - age_hours)
    
    def score_type(self) -> float:
        t = self.type.upper()
        return 50 if t == "R" else 30 if t == "N" else 10
    
class NotamSorter:
    def __init__(self, notams: list[Notam]):
        self.notams = notams

    def sort_by_score(self) -> list[Notam]:
        """
        Sort the NOTAMs by their computed score in descending order.
        """
        return sorted(self.notams, key = lambda x: x.score, reverse=True)