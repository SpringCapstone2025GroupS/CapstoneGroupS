import pytest
from datetime import datetime, timedelta, UTC
from sorting_algorithm import Notam, NotamSorter

@pytest.fixture
def sample_notam_1():
    now = datetime.now(UTC)
    return Notam(
        id="001",
        number="A1234/24",
        type="R",
        issued=now - timedelta(hours=5),
        selection_code=None,
        location="JFK",
        effective_start=now - timedelta(hours=1),
        effective_end=now + timedelta(hours=5),
        text="Runway 13L closed for emergency repairs",
        maximumFL="350",
        classification="Safety",
        account_id="test",
        last_updated=now,
        icao_location="KJFK",
    )

@pytest.fixture
def sample_notam_2():
    now = datetime.now(UTC)
    return Notam(
        id="002",
        number="B5678/24",
        type="N",
        issued=now - timedelta(hours=10),
        selection_code=None,
        location="LAX",
        effective_start=now - timedelta(hours=2),
        effective_end=now + timedelta(hours=3),
        text="Taxiway B closed for maintenance",
        maximumFL="250",
        classification="Maintenance",
        account_id="test",
        last_updated=now,
        icao_location="KLAX",
    )

@pytest.fixture
def sample_notam_3():
    now = datetime.now(UTC)
    return Notam(
        id="003",
        number="C9101/24",
        type="O",
        issued=now - timedelta(hours=2),
        selection_code=None,
        location="ORD",
        effective_start=now - timedelta(hours=1),
        effective_end=now + timedelta(hours=1),
        text="Obstacle near runway 22L",
        maximumFL="150",
        classification="Obstacle",
        account_id="test",
        last_updated=now,
        icao_location="KORD",
    )

def test_max_flight_level(sample_notam_1: Notam):
    assert sample_notam_1.get_max_flight_level() == 350

def test_duration_score(sample_notam_1: Notam):
    duration = sample_notam_1.effective_end - sample_notam_1.effective_start
    expected_hours = duration.total_seconds() / 3600
    assert sample_notam_1.score_duration() == pytest.approx(expected_hours)

def test_recency_score(sample_notam_1:Notam):
    # issued was 5 hours ago, so score should be 19
    assert sample_notam_1.score_recency() == pytest.approx(19.0)

def test_type_score(sample_notam_1: Notam):
    assert sample_notam_1.score_type() == 50

def test_total_score(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam):
    total_score_1 = (
        sample_notam_1.score_duration() +
        sample_notam_1.score_recency() +
        sample_notam_1.score_type()
    )
    total_score_2 = (
        sample_notam_2.score_duration() +
        sample_notam_2.score_recency() +
        sample_notam_2.score_type()
    )
    total_score_3 = (
        sample_notam_3.score_duration() +
        sample_notam_3.score_recency() +
        sample_notam_3.score_type()
    )
    print(f"Total Score: {total_score_1}, {total_score_2}, {total_score_3}")  # Debugging output
    assert sample_notam_1.score == pytest.approx(total_score_1)
    assert sample_notam_2.score == pytest.approx(total_score_2)
    assert sample_notam_3.score == pytest.approx(total_score_3)

def test_sort_by_score(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam):
    notams = [sample_notam_3, sample_notam_1, sample_notam_2]
    sorter = NotamSorter(notams)
    sorted_notams = sorter.sort_by_score()

    # Print the IDs of the sorted NOTAMs for debugging
    sorted_ids = [notam.id for notam in sorted_notams]
    print(f"Sorted NOTAM IDs by score: {sorted_ids}")

    # Ensure the NOTAMs are sorted in descending order of score
    scores = [notam.score for notam in sorted_notams]
    assert scores == sorted(scores, reverse=True)
