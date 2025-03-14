# type: ignore
import pandas as pd
import os

class AirportData:
    columns = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", 
               "Altitude", "Timezone", "DST", "Tz Database Timezone", "Type", "Source"]
    
    try:
        df = pd.read_csv("airports_data.csv", names=columns, header=None)
    except Exception as e:
        df = None

    @staticmethod
    def _get_airport_info(airport_code: str, column: str):
        '''
        Helper method to retrieve airport information by code.

        Args:
            airport_code (str): Airport code (IATA or ICAO).
            column (str): The column name to retrieve.

        Returns:
            Any: The value from the specified column.

        Raises:
            RuntimeError: If the airport data file is missing or empty.
            ValueError: If the airport code is not found or the requested value is missing.
        '''
        if AirportData.df is None or AirportData.df.empty:
            raise RuntimeError("airports_data is not available. Check if the file exists and is correctly formatted.")

        airport = AirportData.df[(AirportData.df["IATA"] == airport_code) | (AirportData.df["ICAO"] == airport_code)]
        if airport.empty:
            raise ValueError(f"Airport code '{airport_code}' not found.")

        value = airport.iloc[0][column]
        if pd.isna(value) or value == "":
            raise ValueError(f"Information for '{column}' is missing for airport code '{airport_code}'.")

        return value

    @staticmethod
    def get_airport_latlong(airport_code: str):
        ''' Retrieves the latitude and longitude of an airport. '''
        return AirportData._get_airport_info(airport_code, "Latitude"), AirportData._get_airport_info(airport_code, "Longitude")

    @staticmethod
    def get_airport_country(airport_code: str):
        ''' Retrieves the country of an airport. '''
        return AirportData._get_airport_info(airport_code, "Country")

    @staticmethod
    def get_airport_timezone(airport_code: str):
        ''' Retrieves the timezone of an airport. '''
        return AirportData._get_airport_info(airport_code, "Tz Database Timezone")