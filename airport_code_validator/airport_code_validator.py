# type: ignore
import pandas as pd
import os

'''
Airport Code Validator Component

Features:
    - Validates if airport code exists and is from the Continental United States
'''
class AirportCodeValidator: 
    @staticmethod
    def is_valid(airport_code: str):
        """
        Validates if airport code is part of Continental United States

        Args:
            airport_code (str): Airport Code Accepting Both IATA and ICAO Format

        Returns:
            True: Valid Continental United States airport
            False: Airport outside Continental United States, or does not exist.
        """
        package_dir = os.path.dirname(__file__)
        airports_file = os.path.join(package_dir, "airports.dat")

        columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz Database Timezone", "Type", "Source"]
        df = pd.read_csv(airports_file, names=columns, header=None)
        airport_details = df[(df["IATA"] == airport_code) | (df["ICAO"] == airport_code)]
        if airport_details.empty or "United States" not in airport_details["Country"].values:
            return False
        return airport_details["Tz Database Timezone"].values[0] not in ["Pacific/Honolulu", "America/Anchorage"]