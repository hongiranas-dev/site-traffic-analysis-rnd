import requests


API_KEY = "lVsmskGlS82eSW91p9f0md8I7aI4LdE0"


def get_traffic_data(latitude, longitude):

    url = (
        "https://api.tomtom.com/traffic/services/4/"
        "flowSegmentData/absolute/10/json"
    )


    params = {
        "point": f"{latitude},{longitude}",
        "unit": "KMPH",
        "key": API_KEY
    }


    response = requests.get(
        url,
        params=params
    )


    data = response.json()


    flow = data["flowSegmentData"]


    current_speed = flow["currentSpeed"]

    free_speed = flow["freeFlowSpeed"]


    congestion_ratio = (
        current_speed / free_speed
    )


    if congestion_ratio < 0.4:

        status = "HIGH TRAFFIC"


    elif congestion_ratio < 0.7:

        status = "MEDIUM TRAFFIC"


    else:

        status = "LOW TRAFFIC"



    return {

        "current_speed": current_speed,

        "free_speed": free_speed,

        "status": status

    }