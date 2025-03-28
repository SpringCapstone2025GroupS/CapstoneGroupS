# type: ignore
import pandas as pd
import os

class AirportData:
    column_names = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", 
               "Altitude", "Timezone", "DST", "Tz Database Timezone", "Type", "Source"]
    
    try:
        df = pd.read_csv("airports.dat", names=column_names, header=None)
    except Exception as e:
        raise RuntimeError("airports_data does not exist or is not in the current directory. Make sure you have run create_airport_data.py to generate the file.")

    @staticmethod
    def _get_airport_info(airport_code: str, column_name: str):
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
        if AirportData.df.empty:
            raise RuntimeError("airports_data is empty. Check if the file exists and is correctly formatted.")

        airport = AirportData.df[(AirportData.df["IATA"] == airport_code) | (AirportData.df["ICAO"] == airport_code)]
        if airport.empty:
            raise ValueError(f"Airport code '{airport_code}' not found in airports_data.")

        value = airport.iloc[0][column_name]
        if pd.isna(value) or value == "":
            raise ValueError(f"Information for '{column_name}' is missing or does not exist for airport code '{airport_code}'.")

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