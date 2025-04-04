# type: ignore
import pandas as pd
import os

from .types import Airport

from typing import Tuple


class AirportData:
    column_names = ["Airport ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", 
               "Altitude", "Timezone", "DST", "Tz Database Timezone", "Type", "Source"]
    
    try:
        df = pd.read_csv("airports.dat", names=column_names, header=1)
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
        if value == "\\N":
            return None
        return value

    @staticmethod
    def get_airport_latlong(airport_code: str) -> Tuple[float, float]:
        ''' Retrieves the latitude and longitude of an airport. '''
        return float(AirportData._get_airport_info(airport_code, "Latitude")), float(AirportData._get_airport_info(airport_code, "Longitude"))

    @staticmethod
    def get_airport_country(airport_code: str) -> str:
        ''' Retrieves the country of an airport. '''
        return AirportData._get_airport_info(airport_code, "Country")

    @staticmethod
    def get_airport_tz_name(airport_code: str) -> str | None:
        ''' Retrieves the timezone of an airport. '''
        return AirportData._get_airport_info(airport_code, "Tz Database Timezone")
    
    @staticmethod
    def get_airport_name(airport_code: str) -> str | None:
        ''' Retrieves the name of an airport. '''
        return AirportData._get_airport_info(airport_code, "Name")

    @staticmethod
    def get_airport_IATA(airport_code: str) -> str | None:
        ''' Retrieves the timezone of an airport. '''
        return AirportData._get_airport_info(airport_code, "IATA")
    
    @staticmethod
    def get_airport_ICAO(airport_code: str) -> str:
        ''' Retrieves the ICAO of an airport. '''
        return AirportData._get_airport_info(airport_code, "ICAO")
    
    @staticmethod
    def get_airport_altitude(airport_code: str) -> int:
        ''' Retrieves the altitude of an airport. '''
        return AirportData._get_airport_info(airport_code, "Altitude")




    @staticmethod
    def get_airport(airport_code: str) -> Airport:
        '''Returns an Airport object for the Airport code'''
        return Airport(
            name=AirportData.get_airport_name(airport_code),
            country = AirportData.get_airport_country(airport_code),
            IATA = AirportData.get_airport_IATA(airport_code),
            ICAO = AirportData.get_airport_ICAO(airport_code),
            coordinates= AirportData.get_airport_latlong(airport_code),
            altitude = AirportData.get_airport_altitude(airport_code),
            tz_name = AirportData.get_airport_tz_name(airport_code)
        )