from dotenv import load_dotenv
import os
import sys


from flight_input_parser import get_flight_input
from airport_code_validator.airport_code_validator import AirportCodeValidator
from flight_path.flight_path import FlightPath
from notam_fetcher import NotamFetcher
from notam_fetcher.api_schema import CoreNOTAMData
from notam_fetcher.exceptions import NotamFetcherRequestError, NotamFetcherUnauthenticatedError
from notam_printer.notam_printer import NotamPrinter
from notam_sorter import NotamSorter





load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
if CLIENT_ID is None:
    sys.exit("Error: CLIENT_ID not set in .env file")
if CLIENT_SECRET is None:
    sys.exit("Error: CLIENT_SECRET not set in .env file")

if __name__ == "__main__":
    """
    Main execution block:
    - Calls get_flight_input() to get user input.
    - Validates the input using AirportCodeValidator.
    - Prints a confirmation message if valid or an error message if invalid.
    """
    # Get user input
    departure_airport, destination_airport = get_flight_input()

    # Validate both airports
    is_valid_dep = AirportCodeValidator.is_valid(departure_airport)
    is_valid_dest = AirportCodeValidator.is_valid(destination_airport)

    if not is_valid_dep or not is_valid_dest:
        sys.exit("Invalid flight input. Please enter valid airport codes.")

    print(f"Fetching Flights from {departure_airport.upper()} to {destination_airport.upper()}.")
    flight_path = FlightPath(departure_code=departure_airport, destination_code=destination_airport)
    waypoints = flight_path.get_waypoints_by_gap(20)
    notam_fetcher = NotamFetcher(CLIENT_ID, CLIENT_SECRET)
    
    all_notams : list[CoreNOTAMData] = []
    for lat, long in waypoints:
        try:
            all_notams.extend(notam_fetcher.fetch_notams_by_latlong(lat, long, 20))
        except NotamFetcherUnauthenticatedError:
            sys.exit("Invalid client_id or secret.")
        except NotamFetcherRequestError:
            sys.exit("Failed to retrieve NOTAMs due to a network issue.")

    notams = [notam.notam for notam in all_notams]

    sorter = NotamSorter(notams)

    sorted_notams = sorter.sort()
    printer = NotamPrinter()
    printer.print_notams(sorted_notams)
