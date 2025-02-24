import argparse

class AirportCodeValidator:
   
    # Set of valid airport codes
    VALID_AIRPORTS = {"JFK", "LAX", "ORD", "DFW", "ATL", "MIA"}

    @staticmethod
    def is_valid(airport_code: str) -> bool:
        """
        Checks if the given airport code is valid.
        
        Args:
            airport_code (str): A three-letter airport code (e.g., "JFK", "LAX").
        
        Returns:
            bool: True if valid, raises ValueError if invalid.
        
        Raises:
            ValueError: If the airport code is not found in the valid set.
        """
        airport_code = airport_code.upper()  # Normalize input to uppercase
        if airport_code not in AirportCodeValidator.VALID_AIRPORTS:
            # If the airport code is not found in the valid set, raise an error
            raise ValueError(f"Invalid airport code: {airport_code}")
        return True  # If valid, return True


def get_flight_input():
    """
    Parses command-line arguments and validates both airport codes.

    Returns:
        tuple: (departure_airport, destination_airport) if valid.
        None: If either airport code is invalid.
    """
    parser = argparse.ArgumentParser(description="Enter departure and destination airport codes.")
    parser.add_argument("departure_airport", type=str, help="3-letter airport code for departure")
    parser.add_argument("destination_airport", type=str, help="3-letter airport code for destination")
    args = parser.parse_args()

    # Convert input to uppercase BEFORE validation
    departure_airport = args.departure_airport.upper()
    destination_airport = args.destination_airport.upper()

    try:
        # Validate both airports
        AirportCodeValidator.is_valid(departure_airport)
        AirportCodeValidator.is_valid(destination_airport)

        return departure_airport, destination_airport  # Return corrected uppercase values
    
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
