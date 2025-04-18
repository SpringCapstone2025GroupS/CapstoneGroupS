# type: ignore
import pandas as pd

from .types import Airport

from typing import Tuple


class AirportData:
    column_names = ["EFF_DATE","SITE_NO","SITE_TYPE_CODE","STATE_CODE","ARPT_ID","CITY","COUNTRY_CODE","REGION_CODE"
                "ADO_CODE","STATE_NAME","COUNTY_NAME","COUNTY_ASSOC_STATE","ARPT_NAME","OWNERSHIP_TYPE_CODE","FACILITY_USE_CODE",
                "LAT_DEG","LAT_MIN","LAT_SEC","LAT_HEMIS","LAT_DECIMAL","LONG_DEG","LONG_MIN","LONG_SEC","LONG_HEMIS","LONG_DECIMAL",
                "SURVEY_METHOD_CODE","ELEV","ELEV_METHOD_CODE","MAG_VARN","MAG_HEMIS","MAG_VARN_YEAR","TPA","CHART_NAME",
                "DIST_CITY_TO_AIRPORT","DIRECTION_CODE","ACREAGE","RESP_ARTCC_ID","COMPUTER_ID","ARTCC_NAME","FSS_ON_ARPT_FLAG",
                "FSS_ID","FSS_NAME","PHONE_NO","TOLL_FREE_NO","ALT_FSS_ID","ALT_FSS_NAME","ALT_TOLL_FREE_NO","NOTAM_ID","NOTAM_FLAG",
                "ACTIVATION_DATE","ARPT_STATUS","FAR_139_TYPE_CODE","FAR_139_CARRIER_SER_CODE","ARFF_CERT_TYPE_DATE","NASP_CODE",
                "ASP_ANLYS_DTRM_CODE","CUST_FLAG","LNDG_RIGHTS_FLAG","JOINT_USE_FLAG","MIL_LNDG_FLAG","INSPECT_METHOD_CODE",
                "INSPECTOR_CODE","LAST_INSPECTION","LAST_INFO_RESPONSE","FUEL_TYPES","AIRFRAME_REPAIR_SER_CODE",
                "PWR_PLANT_REPAIR_SER","BOTTLED_OXY_TYPE","BULK_OXY_TYPE","LGT_SKED","BCN_LGT_SKED","TWR_TYPE_CODE",
                "SEG_CIRCLE_MKR_FLAG","BCN_LENS_COLOR","LNDG_FEE_FLAG","MEDICAL_USE_FLAG","ARPT_PSN_SOURCE","POSITION_SRC_DATE",
                "ARPT_ELEV_SOURCE","ELEVATION_SRC_DATE","CONTR_FUEL_AVBL","TRNS_STRG_BUOY_FLAG","TRNS_STRG_HGR_FLAG",
                "TRNS_STRG_TIE_FLAG","OTHER_SERVICES","WIND_INDCR_FLAG","ICAO_ID","MIN_OP_NETWORK","USER_FEE_FLAG","CTA"]

    try:
        #df = pd.read_csv("airports.dat", names=column_names, header=1)
        df = pd.read_csv("APT_BASE.csv", names=column_names, header=0)
        print(df.head())
    except Exception as e:
        #raise RuntimeError("airports_data does not exist or is not in the current directory.")
        raise RuntimeError("APT_BASE.csv does not exist or is not in the current directory.")

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
            #raise RuntimeError("airports_data is empty. Check if the file exists and is correctly formatted.")
            raise RuntimeError("APT_BASE.csv is empty. Check if the file exists and is correctly formatted.")

        airport = AirportData.df[(AirportData.df["ARPT_ID"] == airport_code) | (AirportData.df["ICAO_ID"] == airport_code)]
        if airport.empty:
            raise ValueError(f"Airport code '{airport_code}' not found in APT_BASE. Check for typos or use a valid code.")

        value = airport.iloc[0][column_name]

        # airport.dat created by 'create_airport_csv.py' encodes null values as '\N'
        #   Accessed columns with null values ('\N')
        #       Tz Database Timezone
        #       IATA
        
        if value == "": 
            return None
        return value

    @staticmethod
    def get_airport_latlong(airport_code: str) -> Tuple[float, float]:
        ''' Retrieves the latitude and longitude of an airport. '''
        return float(AirportData._get_airport_info(airport_code, "LAT_DECIMAL")), float(AirportData._get_airport_info(airport_code, "LONG_DECIMAL"))

    @staticmethod
    def get_airport_country(airport_code: str) -> str:
        ''' Retrieves the country of an airport. '''
        return AirportData._get_airport_info(airport_code, "COUNTRY_CODE")

    @staticmethod
    def get_airport_state_name(airport_code: str) -> str | None:
        ''' Retrieves the state name of an airport. '''
        return AirportData._get_airport_info(airport_code, "STATE_NAME")

    @staticmethod
    def get_airport_name(airport_code: str) -> str | None:
        ''' Retrieves the name of an airport. '''
        return AirportData._get_airport_info(airport_code, "ARPT_NAME")

    @staticmethod
    def get_airport_iata(airport_code: str) -> str | None:
        ''' Retrieves the IATA of an airport. '''
        return AirportData._get_airport_info(airport_code, "ARPT_ID")

    @staticmethod
    def get_airport_icao(airport_code: str) -> str:
        ''' Retrieves the ICAO of an airport. '''
        return AirportData._get_airport_info(airport_code, "ICAO_ID")

    @staticmethod
    def get_airport_elevation(airport_code: str) -> int:
        ''' Retrieves the elevation of an airport. '''
        return int(AirportData._get_airport_info(airport_code, "ELEV"))

    @staticmethod
    def get_airport(airport_code: str) -> Airport:
        '''
        Returns an Airport object for the Airport code
        Args:
            airport_code (str): Airport code (IATA or ICAO).

        Returns:
            Airport: The airport associated with the code.

        Raises:
            ValueError: If the airport code is not found.

        '''
        return Airport(
            name=AirportData.get_airport_name(airport_code),
            country=AirportData.get_airport_country(airport_code),
            iata=AirportData.get_airport_iata(airport_code),
            icao=AirportData.get_airport_icao(airport_code),
            coordinates=AirportData.get_airport_latlong(airport_code),
            elevation=AirportData.get_airport_elevation(airport_code),
            state_name=AirportData.get_airport_state_name(airport_code),
        )