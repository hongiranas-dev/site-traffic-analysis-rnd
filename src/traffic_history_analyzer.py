from dotenv import load_dotenv

load_dotenv()
import os
import json
from datetime import datetime

import osmnx as ox

from osm_extractor import extract_roads
from traffic_api import get_traffic_data


HISTORY_FILE = "outputs/traffic_history.json"


def get_time_period():
    hour = datetime.now().hour

    if 6 <= hour < 10:
        return "MORNING"
    elif 10 <= hour < 16:
        return "DAY"
    elif 16 <= hour < 20:
        return "EVENING"
    else:
        return "NIGHT"


def analyze_traffic_history(graph):

    _, edges = ox.graph_to_gdfs(graph)

    important_roads = [
        "primary",
        "secondary",
        "tertiary",
        "trunk",
        "motorway"
    ]

    history_data = {}

    # Load old history instead of deleting it
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history_data = json.load(f)

    current_period = get_time_period()
    current_time = datetime.now().isoformat()

    for index, road in edges.iterrows():

        road_type = road.get("highway", "unknown")

        if isinstance(road_type, list):
            road_type = road_type[0]

        if road_type not in important_roads:
            continue

        road_name = road.get("name", "Unnamed Road")

        if str(road_name) == "nan" or not road_name:
            road_name = "Unnamed Road"

        road_name = str(road_name)

        geometry = road["geometry"]

        midpoint = geometry.interpolate(
            0.5,
            normalized=True
        )

        latitude = midpoint.y
        longitude = midpoint.x

        traffic = get_traffic_data(
            latitude,
            longitude
        )

        if road_name not in history_data:
            history_data[road_name] = []

        history_data[road_name].append({
            "timestamp": current_time,
            "period": current_period,
            "traffic_status": traffic["status"],
            "current_speed": traffic["current_speed"],
            "free_flow_speed": traffic["free_speed"]
        })

    os.makedirs("outputs", exist_ok=True)

    with open(HISTORY_FILE, "w") as f:
        json.dump(
            history_data,
            f,
            indent=4
        )

    print("\n===== TRAFFIC HISTORY =====")
    print("Current period:", current_period)
    print("History saved successfully")
    print("File:", HISTORY_FILE)


if __name__ == "__main__":

    print("Starting traffic history analysis...")

    road_graph = extract_roads()

    analyze_traffic_history(road_graph)