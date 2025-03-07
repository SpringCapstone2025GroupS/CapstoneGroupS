import argparse
import logging


# Configure logging to track validation attempts and errors
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class AirportCodeValidator:
    """Validates airport codes based on a predefined list of valid airports."""

    # Set of valid airport codes
    VALID_AIRPORTS = {"JFK", "LAX", "ORD", "DFW", "ATL", "MIA"}

    @staticmethod
    def is_valid(airport_code: str):
        """
        Checks if the given airport code is valid.
        
        Args:
            airport_code (str): A three-letter airport code (e.g., "JFK", "LAX").
        
        Raises:
            ValueError: If the airport code is not found in the valid set.
        """
        if airport_code.upper() not in AirportCodeValidator.VALID_AIRPORTS:
            logging.error(f"Invalid airport code entered: {airport_code}")
            raise ValueError(f"Invalid airport code: {airport_code}")

        logging.info(f"Validated airport code: {airport_code}")


def get_flight_input():
    """
    Parses command-line arguments to retrieve departure and destination airport codes.

    Returns:
        tuple: (departure_airport, destination_airport) as raw user input.
    """
    parser = argparse.ArgumentParser(description="Enter departure and destination airport codes.")
    parser.add_argument("departure_airport", type=str, help="3-letter airport code for departure")
    parser.add_argument("destination_airport", type=str, help="3-letter airport code for destination")
    args = parser.parse_args()

    return args.departure_airport, args.destination_airport


if __name__ == "__main__":
    """
    Main execution block:
    - Calls get_flight_input() to get user input.
    - Validates the input using AirportCodeValidator.
    - Prints a confirmation message if valid or an error message if invalid.
    """
    try:
        # Get user input
        departure_airport, destination_airport = get_flight_input()

        # Validate both airports
        AirportCodeValidator.is_valid(departure_airport)
        AirportCodeValidator.is_valid(destination_airport)

        print(f"Flight from {departure_airport.upper()} to {destination_airport.upper()} is valid!")

    except ValueError:
        print("Invalid flight input. Please enter valid airport codes.")
