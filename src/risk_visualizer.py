import json
import folium
import os



def get_color(risk):


    if risk == "HIGH RISK":

        return "red"


    elif risk == "MEDIUM RISK":

        return "orange"


    else:

        return "green"




def create_map():


    with open(
        "outputs/traffic_report.json",
        "r"
    ) as file:


        roads = json.load(file)



    traffic_map = folium.Map(

        location=[
            13.1168,
            77.6347
        ],

        zoom_start=15

    )



    for road in roads:


        popup = f"""

        <b>{road['road_name']}</b><br>

        Type: {road['road_type']}<br>

        Current Speed:
        {road['current_speed']} km/h<br>

        Free Flow:
        {road['free_flow_speed']} km/h<br>

        Traffic:
        {road['traffic_status']}<br>

        Risk:
        {road['risk_score']}/100<br><br>

        {road['architect_insight']}

        """



        folium.CircleMarker(

            location=[

                road["latitude"],

                road["longitude"]

            ],

            radius=8,

            color=get_color(
                road["risk_level"]
            ),

            fill=True,

            popup=popup


        ).add_to(

            traffic_map

        )



    os.makedirs(
        "outputs",
        exist_ok=True
    )


    traffic_map.save(

        "outputs/risk_map.html"

    )


    print(
        "Risk map generated successfully"
    )





if __name__ == "__main__":


    create_map()