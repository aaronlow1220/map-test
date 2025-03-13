import os
from dotenv import load_dotenv
import requests

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAP_API_KEY")


def getDistance(origin: str, destination: str):
    url = f"https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix"
    obj = {
        "origins": [
            {
                "waypoint": {
                    "location": {
                        "latLng": {"latitude": 37.420761, "longitude": -122.081356}
                    }
                },
                "routeModifiers": {"avoid_ferries": True},
            },
            {
                "waypoint": {
                    "location": {
                        "latLng": {"latitude": 37.403184, "longitude": -122.097371}
                    }
                },
                "routeModifiers": {"avoid_ferries": True},
            },
        ],
        "destinations": [
            {
                "waypoint": {
                    "location": {
                        "latLng": {"latitude": 37.420999, "longitude": -122.086894}
                    }
                }
            },
            {
                "waypoint": {
                    "location": {
                        "latLng": {"latitude": 37.383047, "longitude": -122.044651}
                    }
                }
            },
        ],
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


if __name__ == "__main__":
    print(getDistance("台北車站", "台北101"))
