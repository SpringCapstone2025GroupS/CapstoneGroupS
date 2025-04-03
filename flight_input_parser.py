import argparse
from airport_code_validator import AirportCodeValidator



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
