from dotenv import load_dotenv
import logging, os, sys, time

from airport_data.airport_data import AirportData
from flight_input_parser.flight_input_parser import FlightInputParser
from airport_code_validator.airport_code_validator import AirportCodeValidator
from flight_path.flight_path import FlightPath
from notam_fetcher import NotamFetcher
from notam_fetcher.api_schema import CoreNOTAMData, Notam
from notam_fetcher.exceptions import NotamFetcherRateLimitError, NotamFetcherRequestError, NotamFetcherUnauthenticatedError
from notam_printer.notam_printer import NotamPrinter

log_format_string = '%(asctime)s [%(name)s] [%(levelname)s] %(message)s'
log_formatter = logging.Formatter(log_format_string)
logging.basicConfig(level=logging.DEBUG, format=log_format_string, force=True)

# Also log to a file
log_file_handler = logging.FileHandler('output.log', mode='w')
log_file_handler.setLevel(logging.DEBUG)
log_file_handler.setFormatter(log_formatter)
logging.getLogger().addHandler(log_file_handler)

# urllib logger is somewhat chatty at debug, force it to info level logs only
logging.getLogger('urllib3.connectionpool').setLevel(logging.INFO)

logger = logging.getLogger("driver")

class NotamSorter:
    """
    Temporary NotamSorter Stub
    """
    def __init__(self, notams: list[Notam]) -> None:
        self.notams = notams
    def sort(self) -> list[Notam]:
        return self.notams 

def main():
    """
    Main execution block:
    - Load environment variables for CLIENT_ID and CLIENT_SECRET
    - Calls get_flight_input() to get user input.
    - Validates the input using AirportCodeValidator.
    - Prints a confirmation message if valid or an error message if invalid.
    - Uses FlightPath to determine flight path.
    - Calls NotamFetcher for each coordinate returned from flight path.
    - Sorts using NOTAM sorter
    - Prints using NotamPrinter
    """

    load_dotenv()
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")

    if CLIENT_ID is None:
        logger.error("CLIENT_ID not set in .env file")
        sys.exit("Error: CLIENT_ID not set in .env file")
    if CLIENT_SECRET is None:
        sys.exit("Error: CLIENT_SECRET not set in .env file")
    # Get user input
    departure_airport_code, destination_airport_code = FlightInputParser.get_flight_input()

    try:
        departure_airport, destination_airport = AirportData.get_airport(departure_airport_code), AirportData.get_airport(destination_airport_code) 
    except ValueError as e:
        sys.exit(str(e))

    is_valid_dep = AirportCodeValidator.is_valid(departure_airport)
    is_valid_dest = AirportCodeValidator.is_valid(destination_airport)

    if not is_valid_dep:
        sys.exit(f"Invalid departure airport {departure_airport}. Please enter valid airport codes.")

    if not is_valid_dest:
        sys.exit(f"Invalid destination airport {destination_airport}. Please enter valid airport codes.")

    logger.info(f"Fetching Flights from {departure_airport.icao} to {destination_airport.icao}")
    flight_path = FlightPath(departure_code=departure_airport.icao, destination_code=destination_airport.icao)
    
    waypoints = flight_path.get_waypoints_by_gap(40)
    notam_fetcher = NotamFetcher(CLIENT_ID, CLIENT_SECRET, timeout=600)
    
    all_notams : list[CoreNOTAMData] = []
    start_time = time.perf_counter()
    try:
        all_notams = notam_fetcher.fetch_notams_by_latlong_list(waypoints, 30)
    except NotamFetcherUnauthenticatedError:
        logging.error("Invalid client_id or secret.")
        sys.exit("Invalid client_id or secret.")
    except NotamFetcherRequestError:
        logging.error("Failed to retrieve NOTAMs due to a network issue.")
        sys.exit("Failed to retrieve NOTAMs due to a network issue.")
    except NotamFetcherRateLimitError:
        logging.error("Failed to retrieve NOTAMs due to rate limits.")
        sys.exit("Failed to retrieve NOTAMs due to rate limits.") 
    except TimeoutError:
        logging.error("Failed to retrieve NOTAMs due to timeout limit.")
        sys.exit("Failed to retrieve NOTAMs due to timeout limit.") 
    end_time = time.perf_counter()

    notams = [notam.notam for notam in all_notams]
    logger.info(f"Fetched {len(notams)} unique NOTAMs in {end_time-start_time:.3f} seconds")

    sorter = NotamSorter(notams)

    sorted_notams = sorter.sort()
    printer = NotamPrinter(max_lines=3)
    printer.print_notams(sorted_notams)

if __name__ == "__main__":
    main()
