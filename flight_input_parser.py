import argparse



# Configure logging to track validation attempts and errors



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

