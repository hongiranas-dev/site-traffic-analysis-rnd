import json
import os
from datetime import datetime

import osmnx as ox

from osm_extractor import extract_roads
from traffic_api import get_traffic_data



def get_time_category():


    current_hour = datetime.now().hour


    if 7 <= current_hour <= 10:

        return "morning_peak"


    elif 17 <= current_hour <= 20:

        return "evening_peak"


    else:

        return "off_peak"




def collect_traffic_history():


    print(
        "\n===== PEAK / OFF-PEAK TRAFFIC COLLECTION ====="
    )


    graph = extract_roads()


    nodes, edges = ox.graph_to_gdfs(
        graph
    )


    important_roads = [

        "primary",
        "secondary",
        "tertiary",
        "trunk",
        "motorway"

    ]


    time_category = get_time_category()


    history_data = {}


    count = 0



    for index, road in edges.iterrows():


        road_type = road.get(
            "highway",
            "unknown"
        )


        if isinstance(
            road_type,
            list
        ):

            road_type = road_type[0]



        if road_type not in important_roads:

            continue



        road_name = road.get(
            "name",
            "Unnamed Road"
        )


        if str(road_name) == "nan":

            road_name = "Unnamed Road"



        geometry = road[
            "geometry"
        ]


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



        history_data[
            road_name
        ] = {


            "road_type":

                road_type,


            "time_category":

                time_category,


            "collected_time":

                str(
                    datetime.now()
                ),


            "current_speed":

                traffic[
                    "current_speed"
                ],


            "free_flow_speed":

                traffic[
                    "free_speed"
                ],


            "traffic_status":

                traffic[
                    "status"
                ]

        }



        print(
            "\nRoad:",
            road_name
        )


        print(
            "Time:",
            time_category
        )


        print(
            "Traffic:",
            traffic["status"]
        )



        count += 1


        if count == 20:

            break




    os.makedirs(

        "outputs",

        exist_ok=True

    )



    with open(

        "outputs/traffic_history.json",

        "w"

    ) as file:


        json.dump(

            history_data,

            file,

            indent=4

        )



    print(
        "\nTraffic history saved"
    )



if __name__ == "__main__":


    collect_traffic_history()