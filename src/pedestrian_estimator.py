import osmnx as ox
import json
import os



def estimate_pedestrian_flow():


    print(
        "\n===== PEDESTRIAN FLOW ESTIMATION ====="
    )


    # Site coordinate (REVA test location)

    latitude = 13.1168

    longitude = 77.6347


    radius = 1000



    tags = {

        "highway": [
            "bus_stop"
        ],

        "railway": [
            "station"
        ],

        "amenity": True,

        "shop": True

    }



    features = ox.features_from_point(

        (
            latitude,
            longitude
        ),

        tags,

        dist=radius

    )



    pedestrian_score = 0


    factors = {

        "bus_stops": 0,

        "public_places": 0,

        "shops": 0

    }



    for index, feature in features.iterrows():



        if feature.get(
            "highway",
            ""
        ) == "bus_stop":


            pedestrian_score += 20


            factors["bus_stops"] += 1




        if feature.get(
            "shop",
            ""
        ) != "":


            pedestrian_score += 5


            factors["shops"] += 1





        if feature.get(
            "amenity",
            ""
        ) != "":


            pedestrian_score += 10


            factors["public_places"] += 1




    if pedestrian_score >= 100:


        level = "HIGH PEDESTRIAN ACTIVITY"


    elif pedestrian_score >= 50:


        level = "MEDIUM PEDESTRIAN ACTIVITY"


    else:


        level = "LOW PEDESTRIAN ACTIVITY"




    result = {


        "pedestrian_score": pedestrian_score,


        "pedestrian_level": level,


        "factors": factors,


        "recommendation":

            "Provide separate pedestrian pathways and safe crossings"

    }




    os.makedirs(

        "outputs",

        exist_ok=True

    )



    with open(

        "outputs/pedestrian_analysis.json",

        "w"

    ) as file:


        json.dump(

            result,

            file,

            indent=4

        )




    print(

        "Pedestrian Score:",

        pedestrian_score

    )


    print(

        "Level:",

        level

    )


    print(

        "Saved outputs/pedestrian_analysis.json"

    )





if __name__ == "__main__":


    estimate_pedestrian_flow()