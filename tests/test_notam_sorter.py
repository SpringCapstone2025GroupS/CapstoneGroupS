import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from notam_sorter import Notam, NotamSorter

class TestNotamSorter(unittest.TestCase):
    def setUp(self):
        """Set up sample NOTAMs for testing"""
        self.sample_notams = [
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
        self.sorter = NotamSorter(self.sample_notams)

    def test_sorting(self):
        """Test if NOTAMs are sorted correctly"""
        sorted_list = self.sorter.sort()
        sorted_numbers = [notam.number for notam in sorted_list]

        # Expected order: Runway NOTAM first, then Taxiway, then by start time
        expected_order = ["A149/24", "A150/24", "A151/24"]

        self.assertEqual(sorted_numbers, expected_order)

if __name__ == "__main__":
    unittest.main()
