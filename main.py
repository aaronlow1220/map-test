import os
import googlemaps
from dotenv import load_dotenv

load_dotenv()

ADDR = "106 台北市大安區敦化南路二段76號16樓"

API_KEY = os.getenv("GOOGLE_MAP_API_KEY")

gmaps = googlemaps.Client(key=API_KEY)


def getCoordinate(address: str):
    geocode_result = gmaps.geocode(address)[0]
    location = geocode_result["geometry"]["location"]
    return location

def getAddress(lat: float, lng: float):
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))[0]
    address = reverse_geocode_result["formatted_address"]
    return address

if __name__ == '__main__':
    # print(getCoordinate(ADDR))
    print(getAddress(25.0291636, 121.5484016))