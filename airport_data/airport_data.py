# type: ignore
import pandas as pd
import os

class AirportData:
    package_dir = os.path.dirname(__file__)
    airports_file = os.path.join(package_dir, "airports.dat")
    columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz Database Timezone", "Type", "Source"]
    df = pd.read_csv(airports_file, names=columns, header=None)

    @staticmethod
    def get_airport_latlong(airport_code: str):
        '''
        Retrieves the latitude and longitude of an airport

        Args:
            airport_code (str): Airport code accepting both IATA and ICAO format.

        Returns:
            tuple: (latitude, longitude), if found

        Raises:
            RuntimeError: If the airport data file is missing or empty.
            ValueError: If the airport code is not found.
        '''
        if AirportData.df is None or AirportData.df.empty:
            raise RuntimeError("Airport data is not available. Check if the file exists and is correctly formatted.")

        airport = AirportData.df[(AirportData.df["IATA"] == airport_code) | (AirportData.df["ICAO"] == airport_code)]
        if not airport.empty:
            return airport.iloc[0]["Latitude"], airport.iloc[0]["Longitude"]
        raise ValueError(f"Airport code '{airport_code}' not found.")

    @staticmethod
    def get_airport_country(airport_code: str):
        '''
        Retrieves the country of an airport

        Args:
            airport_code (str): Airport code accepting both IATA and ICAO format.

        Returns:
            str: Country name, if found

        Raises:
            RuntimeError: If the airport data file is missing or empty.
            ValueError: If the airport code is not found.
        '''
        if AirportData.df is None or AirportData.df.empty:
            raise RuntimeError("Airport data is not available. Check if the file exists and is correctly formatted.")

        airport = AirportData.df[(AirportData.df["IATA"] == airport_code) | (AirportData.df["ICAO"] == airport_code)]
        if not airport.empty:
            return airport.iloc[0]["Country"]
        raise ValueError(f"Airport code '{airport_code}' not found.")

    @staticmethod
    def get_airport_timezone(airport_code: str):
        '''
        Retrieves the timezone of an airport

        Args:
            airport_code (str): Airport code accepting both IATA and ICAO format.

        Returns:
            str: Tz Database Timezone, if found

        Raises:
            RuntimeError: If the airport data file is missing or empty.
            ValueError: If the airport code is not found.
        '''
        if AirportData.df is None or AirportData.df.empty:
            raise RuntimeError("Airport data is not available. Check if the file exists and is correctly formatted.")

        airport = AirportData.df[(AirportData.df["IATA"] == airport_code) | (AirportData.df["ICAO"] == airport_code)]
        if not airport.empty:
            return airport.iloc[0]["Tz Database Timezone"]
        raise ValueError(f"Airport code '{airport_code}' not found.")