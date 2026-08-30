import os

import requests


def get_traffic_data(latitude, longitude):

    api_key = os.getenv("TOMTOM_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Set TOMTOM_API_KEY in your environment before using TomTom."
        )

    url = (
        "https://api.tomtom.com/traffic/services/4/"
        "flowSegmentData/absolute/10/json"
    )

    params = {
        "point": f"{latitude},{longitude}",
        "unit": "KMPH",
        "key": api_key
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    flow = data["flowSegmentData"]

    current_speed = flow["currentSpeed"]
    free_speed = flow["freeFlowSpeed"]

    congestion_ratio = (
        current_speed / free_speed
    )

    if congestion_ratio < 0.65:
        status = "HIGH TRAFFIC"

    elif congestion_ratio < 0.85:
        status = "MEDIUM TRAFFIC"

    else:
        status = "LOW TRAFFIC"

    return {
        "current_speed": current_speed,
        "free_speed": free_speed,
        "status": status
    }