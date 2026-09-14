import os
import json
import requests
from datetime import datetime, timedelta

from dotenv import load_dotenv

load_dotenv()

TOMTOM_API_KEY = os.getenv("TOMTOM_API_KEY")

CACHE_FILE = "outputs/tomtom_cache.json"
CACHE_MINUTES = 15


def get_cache():

    if os.path.exists(CACHE_FILE):

        with open(CACHE_FILE, "r") as file:
            return json.load(file)

    return {}


def save_cache(cache):

    os.makedirs("outputs", exist_ok=True)

    with open(CACHE_FILE, "w") as file:
        json.dump(cache, file, indent=4)


def get_traffic_data(latitude, longitude):

    if not TOMTOM_API_KEY:
        raise RuntimeError(
            "Set TOMTOM_API_KEY in your environment before using TomTom."
        )

    location_key = f"{latitude:.5f},{longitude:.5f}"

    cache = get_cache()

    # Use cache if it is still fresh
    if location_key in cache:

        cached_time = datetime.fromisoformat(
            cache[location_key]["timestamp"]
        )

        if datetime.now() - cached_time < timedelta(
            minutes=CACHE_MINUTES
        ):

            print("Using cached TomTom data:", location_key)

            return cache[location_key]["data"]

    # TomTom API
    url = (
        "https://api.tomtom.com/traffic/services/4/"
        "flowSegmentData/relative/10/json"
    )

    params = {
        "point": f"{latitude},{longitude}",
        "key": TOMTOM_API_KEY
    }

    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    flow_data = data["flowSegmentData"]

    current_speed = flow_data["currentSpeed"]
    free_speed = flow_data["freeFlowSpeed"]

    congestion_ratio = current_speed / free_speed

    if congestion_ratio < 0.65:
        status = "HIGH TRAFFIC"
    elif congestion_ratio < 0.85:
        status = "MEDIUM TRAFFIC"
    else:
        status = "LOW TRAFFIC"

    result = {
        "current_speed": current_speed,
        "free_speed": free_speed,
        "status": status
    }

    # Save fresh result
    cache[location_key] = {
        "timestamp": datetime.now().isoformat(),
        "data": result
    }

    save_cache(cache)

    print("Fresh TomTom data fetched:", location_key)

    return result