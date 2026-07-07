import json
import os


SITE_LAT = 13.1168
SITE_LON = 77.6347



def find_direction(lat, lon):


    vertical = ""

    horizontal = ""



    if lat > SITE_LAT:

        vertical = "North"


    else:

        vertical = "South"



    if lon > SITE_LON:

        horizontal = "East"


    else:

        horizontal = "West"



    return vertical + "-" + horizontal




def analyze_directions():


    with open(
        "outputs/traffic_report.json",
        "r"
    ) as file:


        roads = json.load(file)



    direction_report = []



    for road in roads:


        direction = find_direction(

            road["latitude"],

            road["longitude"]

        )



        data = {


            "road_name": road["road_name"],


            "direction": direction,


            "risk_level": road["risk_level"],


            "recommendation":

                "Avoid entry here"

                if road["risk_level"] == "HIGH RISK"

                else

                "Possible entry side"

        }



        direction_report.append(

            data

        )



        print(

            road["road_name"],

            "=>",

            direction,

            "|",

            data["recommendation"]

        )




    os.makedirs(

        "outputs",

        exist_ok=True

    )



    with open(

        "outputs/direction_analysis.json",

        "w"

    ) as file:


        json.dump(

            direction_report,

            file,

            indent=4

        )




    print(

        "\nSaved outputs/direction_analysis.json"

    )




if __name__ == "__main__":


    analyze_directions()