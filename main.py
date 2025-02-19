from dotenv import load_dotenv
import os
import sys


from notam_fetcher import NotamFetcher

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

if CLIENT_ID is None:
    sys.exit("Error: CLIENT_ID not set in .env file")
if CLIENT_SECRET is None:
    sys.exit("Error: CLIENT_SECRET not set in .env file")

notam_fetcher = NotamFetcher(CLIENT_ID, CLIENT_SECRET)

notams = notam_fetcher.fetch_notams_by_latlong(22, -78, 100)  

