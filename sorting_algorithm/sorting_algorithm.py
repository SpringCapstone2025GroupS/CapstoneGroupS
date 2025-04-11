from notam_fetcher.api_schema import Notam, PurposeType

class NotamSorter:
    def __init__(self, notams: list[Notam]):
        self.notams = notams

    def score_by_purpose(self, notam: Notam) -> float:
        """
        Assigns a base score based on PurposeType.
        N = 50, B = 25, O = 10, M = 5
        """
        if PurposeType.N in notam.purpose:
            return 50
        elif PurposeType.B in notam.purpose:
            return 25
        elif PurposeType.O in notam.purpose:
            return 10
        elif PurposeType.M in notam.purpose:
            return 5
        else:
            return 0

    def score(self, notam: Notam) -> float:
        """
        Calculates the total score for a NOTAM by combining multiple scoring functions.
        """
        total_score = 0.0
        total_score += self.score_by_purpose(notam)
        # Add other scoring functions here, e.g.:
        # total_score += self.score_by_duration(notam)
        # total_score += self.score_by_recency(notam)
        return total_score

    def sort_by_score(self) -> list[Notam]:
        """
        Sorts the NOTAMs in descending order of their scores.
        """
        return sorted(self.notams, key=self.score, reverse=True)