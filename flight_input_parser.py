import argparse

class AirportCodeValidator:
    @staticmethod
    def is_valid(airport_code):
        # Checks if the given airport code is valid 
        # Set of valid airport codes, airport_code (str): A three-letter airport code (e.g., "JFK", "LAX")
        valid_airports = {"JFK", "LAX", "ORD", "DFW", "ATL", "MIA"}
        if airport_code not in valid_airports:
            # If the airport code is not found in the valid set, raise an error
            raise ValueError(f"Invalid airport code: {airport_code}")
        return True # If valid, return True

def get_flight_input():
    """
    Parses command-line arguments and validates both airport codes.

    This function:
    1. Reads user input from the command line.
    2. Validates the departure and destination airport codes.
    3. Returns a tuple (departure, destination) if both are valid.
    4. Returns None if any airport code is invalid.

    Returns:
        tuple: (departure_airport, destination_airport) if valid.
        None: if either airport code is invalid.
    """

    # argparse is a built-in Python module for handling command-line arguments.
    parser = argparse.ArgumentParser(description="Enter departure and destination airport codes.")

    # Adding expected command-line arguments (departure and destination airport codes)
    parser.add_argument("departure_airport", type=str, help="3-letter airport code for departure")
    parser.add_argument("destination_airport", type=str, help="3-letter airport code for destination")

    args = parser.parse_args()

    try:
        # Validate BOTH airports before proceeding
         # If either is invalid, an exception will be raised, and execution jumps to the except block.
        is_departure_valid = AirportCodeValidator.is_valid(args.departure_airport)
        is_destination_valid = AirportCodeValidator.is_valid(args.destination_airport)

        if is_departure_valid and is_destination_valid:
            # If both validations pass, return them as a tuple.
            return args.departure_airport, args.destination_airport
    except ValueError as e:
        print(f"Error: {e}")  # Log the error
        return None  # Return None if either airport is invalid

if __name__ == "__main__":
    """
    Main execution block:
    - Calls get_flight_input() to get and validate user input.
    - If the input is valid, prints a confirmation message.
    - If the input is invalid, prints an error message.
    """
    flight_info = get_flight_input()
    if flight_info:
        print(f"Flight from {flight_info[0]} to {flight_info[1]} is valid!")
    else:
        print("Invalid flight input. Please enter valid airport codes.")
