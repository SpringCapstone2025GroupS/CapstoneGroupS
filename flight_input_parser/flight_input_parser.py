import argparse

"""
Flight Input Parser Component 

Features:
    - Parses Airport codes, and uses the isValid feature from airportCodeValidator, to validate them, and return a tuple of the airport codes.

"""
class FlightInputParser:
    @staticmethod
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
