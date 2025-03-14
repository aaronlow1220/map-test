import os
import googlemaps
from dotenv import load_dotenv
import requests
import numpy as np

load_dotenv()

API_KEY = os.getenv("GOOGLE_MAP_API_KEY")

gmaps = googlemaps.Client(key=API_KEY)


def extract_distance_matrix(data, num_locations):
    matrix = np.full((num_locations, num_locations), np.inf)

    for entry in data:
        origin = entry["originIndex"]
        dest = entry["destinationIndex"]
        if "distanceMeters" in entry:
            matrix[origin][dest] = entry["distanceMeters"]

    return matrix


def solve_tsp_nearest_neighbor(matrix):
    num_locations = len(matrix)
    visited = [False] * num_locations
    path = [0]  # Start from node 0
    visited[0] = True
    total_cost = 0

    for _ in range(num_locations - 1):
        last = path[-1]
        next_city = None
        min_distance = float("inf")

        for city in range(num_locations):
            if not visited[city] and matrix[last][city] < min_distance:
                min_distance = matrix[last][city]
                next_city = city

        if next_city is not None:
            path.append(next_city)
            visited[next_city] = True
            total_cost += min_distance

    # Return to starting point
    total_cost += matrix[path[-1]][path[0]]
    path.append(path[0])

    return path, total_cost


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
        "X-Goog-FieldMask": "originIndex,destinationIndex,duration,distanceMeters,condition",
    }

    response = requests.post(url, headers=headers, json=obj)
    distance = response.json()
    return distance


def getOptimalRoute(waypoints: set):
    return 1


def main():
    route = [
        {
            "originIndex": 0,
            "destinationIndex": 0,
            "duration": "0s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 1,
            "destinationIndex": 1,
            "duration": "0s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 0,
            "destinationIndex": 1,
            "distanceMeters": 5256,
            "duration": "929s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 2,
            "destinationIndex": 2,
            "duration": "0s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 1,
            "destinationIndex": 0,
            "distanceMeters": 6328,
            "duration": "1031s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 3,
            "destinationIndex": 0,
            "distanceMeters": 4130,
            "duration": "673s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 3,
            "destinationIndex": 3,
            "duration": "0s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 0,
            "destinationIndex": 3,
            "distanceMeters": 3475,
            "duration": "730s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 1,
            "destinationIndex": 3,
            "distanceMeters": 6067,
            "duration": "1186s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 2,
            "destinationIndex": 1,
            "distanceMeters": 4724,
            "duration": "930s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 0,
            "destinationIndex": 2,
            "distanceMeters": 9768,
            "duration": "1588s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 1,
            "destinationIndex": 2,
            "distanceMeters": 4442,
            "duration": "1080s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 2,
            "destinationIndex": 0,
            "distanceMeters": 10995,
            "duration": "1365s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 3,
            "destinationIndex": 1,
            "distanceMeters": 5334,
            "duration": "847s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 2,
            "destinationIndex": 3,
            "distanceMeters": 6319,
            "duration": "1232s",
            "condition": "ROUTE_EXISTS",
        },
        {
            "originIndex": 3,
            "destinationIndex": 2,
            "distanceMeters": 6295,
            "duration": "1081s",
            "condition": "ROUTE_EXISTS",
        },
    ]


    places = {"台北車站", "台北101", "松山機場", "台北橋"}
    # route = getWaypointsDistance(places)

    num_locations = 4  # Based on the max index from the data

    matrix = extract_distance_matrix(route, num_locations)

    tsp_path, tsp_cost = solve_tsp_nearest_neighbor(matrix)

    print("Approximate TSP Path (Nearest Neighbor):", tsp_path)
    print("Total Distance:", tsp_cost, "meters")
    print(matrix)

# print(getWaypointsDistance(places))


if __name__ == "__main__":
    main()
