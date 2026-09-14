import osmnx as ox
import json
import os

from config import SITE_LAT, SITE_LON, SEARCH_RADIUS


def analyze_traffic_signals():

    print("\n===== TRAFFIC SIGNAL ANALYSIS =====")
    print("Site:", SITE_LAT, SITE_LON)
    print("Radius:", SEARCH_RADIUS)

    ox.settings.requests_timeout = 120

    tags = {
        "highway": "traffic_signals"
    }

    try:

        print("Searching OpenStreetMap for traffic signals...")

        signals = ox.features_from_point(
            (SITE_LAT, SITE_LON),
            tags,
            dist=SEARCH_RADIUS
        )

        print("OpenStreetMap response received.")

    except Exception as e:

        print("\nERROR: Could not get traffic signals from OpenStreetMap.")
        print("Reason:", e)

        return

    signal_data = []

    for index, signal in signals.iterrows():

        geometry = signal.geometry

        if geometry.geom_type == "Point":
            signal_lat = geometry.y
            signal_lon = geometry.x
        else:
            center = geometry.centroid
            signal_lat = center.y
            signal_lon = center.x

        signal_data.append({
            "latitude": signal_lat,
            "longitude": signal_lon,
            "type": "traffic_signal"
        })

        print("Signal found:", signal_lat, signal_lon)

    os.makedirs("outputs", exist_ok=True)

    with open("outputs/traffic_signals.json", "w") as file:
        json.dump(signal_data, file, indent=4)

    print("\nTotal Signals Found:", len(signal_data))
    print("Saved: outputs/traffic_signals.json")


if __name__ == "__main__":
    analyze_traffic_signals()