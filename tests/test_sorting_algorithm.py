import pytest
from datetime import datetime, timedelta, UTC
from notam_fetcher.api_schema import Notam, PurposeType, NotamType, Classification, ScopeType, Series
from sorting_algorithm.sorting_algorithm import NotamSorter, score_by_purpose, score, score_by_type, score_by_classification, score_by_category_scope

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

@pytest.fixture
def sample_notam_4():
    now = datetime.now(UTC)
    return Notam(
        id="004",
        number="D2345/24",
        type=NotamType.R,
        issued=now - timedelta(hours=1),
        purpose={PurposeType.M},
        location="SFO",
        effective_start=now,
        effective_end=now + timedelta(hours=4),
        text="Emergency obstacle on runway 28",
        classification=Classification.MIL,
        account_id="test",
        last_updated=now,
        icao_location="KSFO",
        series=Series.R,
        scope={ScopeType.A, ScopeType.W},
    )

@pytest.fixture
def sample_notam_5():
    now = datetime.now(UTC)
    return Notam(
        id="005",
        number="E3456/24",
        type=NotamType.C,
        issued=now - timedelta(hours=3),
        purpose={PurposeType.O},
        location="MIA",
        effective_start=now - timedelta(hours=1),
        effective_end=now + timedelta(hours=2),
        text="Navigational aid out of service enroute",
        classification=Classification.LMIL,
        account_id="test",
        last_updated=now,
        icao_location="KMIA",
        series=Series.C,
        scope={ScopeType.E},
    )

def test_score_by_purpose(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam, sample_notam_4: Notam, sample_notam_5: Notam):
    assert score_by_purpose(sample_notam_1) == 50  # PurposeType.N
    assert score_by_purpose(sample_notam_2) == 25  # PurposeType.B
    assert score_by_purpose(sample_notam_3) == 10  # PurposeType.O
    assert score_by_purpose(sample_notam_4) == 5   # M
    assert score_by_purpose(sample_notam_5) == 10  # O

def test_score_by_type(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam, sample_notam_4: Notam, sample_notam_5: Notam):
    assert score_by_type(sample_notam_1) == 20  # NotamType.N
    assert score_by_type(sample_notam_2) == 20  # NotamType.N
    assert score_by_type(sample_notam_3) == 20  # NotamType.N
    assert score_by_type(sample_notam_4) == 50  # NotamType.R
    assert score_by_type(sample_notam_5) == 10  # NotamType.C

def test_score_by_classification(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam, sample_notam_4: Notam, sample_notam_5: Notam):
    assert score_by_classification(sample_notam_1) == 0  # FDC
    assert score_by_classification(sample_notam_2) == 0  # FDC
    assert score_by_classification(sample_notam_3) == 0  # FDC
    assert score_by_classification(sample_notam_4) == 10  # MIL
    assert score_by_classification(sample_notam_5) == 10  # LMIL

def test_score_by_category_scope(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam, sample_notam_4: Notam, sample_notam_5: Notam):
    assert score_by_category_scope(sample_notam_1) == 0  # No series or scope
    assert score_by_category_scope(sample_notam_2) == 0  # No series or scope
    assert score_by_category_scope(sample_notam_3) == 0  # No series or scope
    assert score_by_category_scope(sample_notam_4) == 45  # Series.R + Scope A and W
    assert score_by_category_scope(sample_notam_5) == 10  # Series.C + Scope E

def test_score(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam, sample_notam_4: Notam, sample_notam_5: Notam):
    sorter = NotamSorter([sample_notam_1, sample_notam_2, sample_notam_3, sample_notam_4, sample_notam_5])
    assert score(sample_notam_1) == 70  # 50+20+0+0
    assert score(sample_notam_2) == 45  # 25+20+0+0
    assert score(sample_notam_3) == 30  # 10+20+0+0
    assert score(sample_notam_4) == 110  # 5+50+10+20+20+5
    assert score(sample_notam_5) == 40   # 10+10+10+10

def test_sort_by_score(sample_notam_1: Notam, sample_notam_2: Notam, sample_notam_3: Notam, sample_notam_4: Notam, sample_notam_5: Notam):
    notams = [sample_notam_2, sample_notam_4, sample_notam_5, sample_notam_1, sample_notam_3]
    sorter = NotamSorter(notams)
    sorted_notams = sorter.sort_by_score()

    # Verify the order of sorted NOTAMs by their scores
    assert [notam.id for notam in sorted_notams] == ["004", "001", "002", "005", "003"]