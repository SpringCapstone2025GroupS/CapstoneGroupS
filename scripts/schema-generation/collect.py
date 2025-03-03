"""
Collects and saves NOTAM responses from the FAA API to be used in genson model generation.

The script does this buy colleting NOTAMs from GPS coordinates starting at the top left and ending the bottom right
We interpolate between the top left and bottom creating a STEPS * STEPS grid where we pull NOTAM data from.  
"""
from dotenv import load_dotenv
import os
import sys
import json
from notam_fetcher import NotamFetcher
from notam_fetcher.notam_fetcher import NotamAirportCodeRequest, NotamLatLongRequest

STEPS = 5
US_TOP_LEFT = {"lat": 47.998332, "long": -123.896002}
US_BOTTOM_RIGHT = {"lat": 33.074457, "long": -80.038583}


def linspace(start: float, stop: float, n:int):
    """
    creates a list of size n from [start, ..., stop] evenly spaced

    Borrowed from: https://stackoverflow.com/questions/12334442/does-python-have-a-linspace-function-in-its-std-lib
    """
    if n == 1:
        yield stop
        return
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i


load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if CLIENT_ID is None:
    sys.exit("Error: CLIENT_ID not set in .env file")
if CLIENT_SECRET is None:
    sys.exit("Error: CLIENT_SECRET not set in .env file")

notam_fetcher = NotamFetcher(CLIENT_ID, CLIENT_SECRET)


os.makedirs('./scripts/data-for-schema-generation/collected/')

# Get API Responses for Lat Long
for lat in linspace(US_TOP_LEFT["lat"], US_BOTTOM_RIGHT["lat"], STEPS):
    for long in linspace(US_TOP_LEFT["long"], US_BOTTOM_RIGHT["long"], STEPS):
        request : NotamLatLongRequest = NotamLatLongRequest(lat, long, 100)
        request.page_num=1
        request.page_size=1000
        response = notam_fetcher._fetch_notams_raw(request)         # type: ignore
        with open(f'./scripts/data-for-schema-generation/collected/response-{lat}-{long}.json', 'w') as file:
            json.dump(response, file)

# Get API Responses for Airport Codes
for airport in ["JFK", "LAX", "ORD", "DFW", "ATL", "MIA"]:

        airport_request : NotamAirportCodeRequest = NotamAirportCodeRequest("LAX")

        airport_request.page_num=1
        airport_request.page_size=1000
        response = notam_fetcher._fetch_notams_raw(request)         # type: ignore
        with open(f'./scripts/data-for-schema-generation/collected/response-airport-code-{airport}.json', 'w') as file:
            json.dump(response, file)





