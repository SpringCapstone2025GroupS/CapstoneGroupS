import pytest
from datetime import datetime, timedelta, UTC
from notam_fetcher.api_schema import Notam, PurposeType, NotamType, Classification
from sorting_algorithm.sorting_algorithm import NotamSorter, score_by_purpose, score

@pytest.fixture
def sample_notam_1():
    now = datetime.now(UTC)
    return Notam(
        id="001",
        number="A1234/24",
        type=NotamType.N,
        issued=now - timedelta(hours=5),
        purpose={PurposeType.N},
        location="JFK",
        effective_start=now - timedelta(hours=1),
        effective_end=now + timedelta(hours=5),
        text="Runway 13L closed for emergency repairs",
        classification=Classification.FDC,
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
        type=NotamType.N,
        issued=now - timedelta(hours=10),
        purpose={PurposeType.B},
        location="LAX",
        effective_start=now - timedelta(hours=2),
        effective_end=now + timedelta(hours=3),
        text="Taxiway B closed for maintenance",
        classification=Classification.FDC,
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
        type=NotamType.N,
        issued=now - timedelta(hours=2),
        purpose={PurposeType.O},
        location="ORD",
        effective_start=now - timedelta(hours=1),
        effective_end=now + timedelta(hours=1),
        text="Obstacle near runway 22L",
        classification=Classification.FDC,
        account_id="test",
        last_updated=now,
        icao_location="KORD",
    )

def test_score_by_purpose(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam):
    assert score_by_purpose(sample_notam_1) == 50  # PurposeType.N
    assert score_by_purpose(sample_notam_2) == 25  # PurposeType.B
    assert score_by_purpose(sample_notam_3) == 10  # PurposeType.O

def test_score(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam):
    sorter = NotamSorter([sample_notam_1, sample_notam_2, sample_notam_3])
    assert score(sample_notam_1) == 50  # Only score_by_purpose is used
    assert score(sample_notam_2) == 25
    assert score(sample_notam_3) == 10

def test_sort_by_score(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam):
    notams = [sample_notam_3, sample_notam_1, sample_notam_2]
    sorter = NotamSorter(notams)
    sorted_notams = sorter.sort_by_score()

    # Verify the order of sorted NOTAMs by their scores
    assert [notam.id for notam in sorted_notams] == ["001", "002", "003"]