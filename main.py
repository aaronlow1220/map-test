import os
import googlemaps
from dotenv import load_dotenv
import requests

load_dotenv()

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


def getDistance(origin: str, destination: str):
    distance_matrix = gmaps.distance_matrix(origin, destination)
    distance = distance_matrix["rows"][0]["elements"][0]["distance"]["text"]
    return distance


def getWaypointsDistance(waypoints: set):
    url = f"https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"

    waypointsList = [{"waypoint": {"address": waypoint}} for waypoint in waypoints]
    obj = {
        "origins": waypointsList,
        "destinations": waypointsList,
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE",
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "originIndex,destinationIndex,duration,distanceMeters,status,condition",
    }

    response = requests.post(url, headers=headers, json=obj)
    distance = response.json()
    return distance


def main():
    places = {"台北車站", "台北101", "松山機場", "台北橋"}

    print(getWaypointsDistance(places))
    # print(getCoordinate(ADDR))
    # print(getAddress(25.0291636, 121.5484016))
    # print(getDistance("台北車站", "台北101"))


if __name__ == "__main__":
    main()
