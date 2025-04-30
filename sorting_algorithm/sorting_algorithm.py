from notam_fetcher.api_schema import Notam, PurposeType, NotamType, Classification, ScopeType, Series

def score_by_purpose(notam: Notam) -> float:
    """
    Assigns a base score based on PurposeType.
    N = 50, B = 25, O = 10, M = 5
    """
    if notam.purpose and PurposeType.N in notam.purpose:
        return 50
    elif notam.purpose and PurposeType.B in notam.purpose:
        return 25
    elif notam.purpose and PurposeType.O in notam.purpose:
        return 10
    elif notam.purpose and PurposeType.M in notam.purpose:
        return 5
    else:
        return 0
    
def score_by_type(notam: Notam) -> float:
    """
    Scores based on NOTAM type: R=50, N=20, other=10.
    Refer to api_schema.py for details on the NotamType enum.
    """
    TYPE_SCORES = {NotamType.R: 50, NotamType.N: 20}
    return TYPE_SCORES.get(notam.type, 10)


def score_by_classification(notam: Notam) -> float:
    """
    Adjusts score for classifications: MIL/LMIL +10, others 0.
    Refer to api_schema.py for details on the Classification enum.
    """
    CLASS_SCORES = {Classification.MIL: 10, Classification.LMIL: 10}
    return CLASS_SCORES.get(notam.classification, 0)


def score_by_category_scope(notam: Notam) -> float:
    """
    Scores based on Series and Scope qualifiers.
    Series.R:+20; Scopes A:+20, E:+10, W:+5, K:+0.
    Refer to api_schema.py for details on the Series and ScopeType enums.
    """
    total = 0.0
    if notam.series == Series.R:
        total += 20
    for scope in (notam.scope or []):
        if scope == ScopeType.A:
            total += 20
        elif scope == ScopeType.E:
            total += 10
        elif scope == ScopeType.W:
            total += 5
    return total

def score(notam: Notam) -> float:
    """
    Calculates the total score for a NOTAM by combining multiple scoring functions.
    """
    total_score = 0.0
    total_score += score_by_purpose(notam)
    total_score += score_by_type(notam)
    total_score += score_by_classification(notam)
    total_score += score_by_category_scope(notam)
    # Add other scoring functions here if needed
    return total_score

class NotamSorter:
    def __init__(self, notams: list[Notam]):
        self.notams = notams

    def sort_by_score(self) -> list[Notam]:
        """
        Sorts the NOTAMs in descending order of their scores.
        """
        return sorted(self.notams, key=score, reverse=True)  # Use the standalone score function