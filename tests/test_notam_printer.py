import sys
import os
import pytest
from pytest import CaptureFixture
from typing import List
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from notam_printer.notam_printer import Notam, NotamPrinter

@pytest.fixture
def sample_notams():
    return [
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
        )
    ]

def test_negative_max_lines():
    with pytest.raises(ValueError):
        printer = NotamPrinter(max_lines=-1)

def test_zero_max_lines():
    with pytest.raises(ValueError):
        printer = NotamPrinter(max_lines=0)

def test_print_max_lines(sample_notams: List[Notam]):
    notam = sample_notams[0]
    # six lines total
    notam.text="test\nmultiline\nnotam\nwith\nmany\nnewlines"
    printer = NotamPrinter(max_lines=3)
    # three lines + '...'
    assert(len(printer.print_notam(notam).split('\n')) == 4)

def test_print_max_lines_more_than_max(sample_notams: List[Notam]):
    notam = sample_notams[0]
    # six lines total
    notam.text="test\nmultiline\nnotam\nwith\nmany\nnewlines"
    printer = NotamPrinter(max_lines=999)
    # not 7 because we don't output '...' if we don't truncate anything
    assert(len(printer.print_notam(notam).split('\n')) == 6)

def test_max_lines_is_none(sample_notams: List[Notam]):
    notam = sample_notams[0]
    # six lines total
    notam.text="test\nmultiline\nnotam\nwith\nmany\nnewlines"
    printer = NotamPrinter(max_lines=None)
    # not 7 because we don't output '...' if we don't truncate anything
    assert(len(printer.print_notam(notam).split('\n')) == 6)
    # the full text should also be printed
    assert(len(printer.print_notam(notam)) == len(notam.text))

def test_print_by_default(sample_notams: List[Notam]):
    notam = sample_notams[0]
    # six lines total
    notam.text="test\nmultiline\nnotam\nwith\nmany\nnewlines"
    printer = NotamPrinter()
    # not 7 because we don't output '...' if we don't truncate anything
    assert(len(printer.print_notam(notam).split('\n')) == 6)
    # the full text should also be printed
    assert(len(printer.print_notam(notam)) == len(notam.text))

def test_print_all_fields(sample_notams: List[Notam]):
    printer = NotamPrinter(print_all_fields=True)
    # Assertions to format for each notam in the list.
    for notam in sample_notams:
        formatted_notam = printer.print_notam(notam)
        assert "ID: " + notam.id in formatted_notam
        assert "Number: " + notam.number in formatted_notam
        assert "Type: " + notam.type in formatted_notam
        assert "Issued: " + notam.issued in formatted_notam
        assert "Location: " + notam.location in formatted_notam
        assert "Effective Start: " + notam.effective_start in formatted_notam
        assert "Effective End: " + notam.effective_end in formatted_notam
        assert "Text: " + notam.text in formatted_notam

def test_print_notams(sample_notams: List[Notam], capsys: CaptureFixture[str]):
    printer = NotamPrinter(print_all_fields=True)
    printer.print_notams(sample_notams)

    # Capture printed output.
    printed_output = capsys.readouterr().out
   
    # Assertions to verify the printed output matches the expected format and content.
    assert "ID: 1" in printed_output, "Number: A150/24" in printed_output
    assert "ID: 2" in printed_output, "Number: A151/24" in printed_output
    assert "ID: 3" in printed_output, "Number: A149/24" in printed_output

