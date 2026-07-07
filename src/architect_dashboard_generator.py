import folium
import json
import os



def load_json(path):

    if os.path.exists(path):

        with open(path, "r") as file:

            return json.load(file)

    return []




def generate_dashboard():


    print("\n===== GENERATING ARCHITECT DASHBOARD =====")


    site_lat = 13.1168
    site_lon = 77.6347


    dashboard = folium.Map(

        location=[site_lat, site_lon],

        zoom_start=15

    )



    # =============================
    # SITE LOCATION
    # =============================


    folium.Marker(

        [site_lat, site_lon],

        popup="PROJECT SITE",

        icon=folium.Icon(

            color="blue",

            icon="home"

        )

    ).add_to(dashboard)





    # =============================
    # TRAFFIC RISK ROADS
    # =============================


    traffic = load_json(

        "outputs/traffic_report.json"

    )


    for road in traffic:


        if road["risk_level"] == "HIGH RISK":

            color = "red"


        elif road["risk_level"] == "MEDIUM RISK":

            color = "orange"


        else:

            color = "green"



        popup = f"""

        <b>Road:</b>{road['road_name']}<br>

        <b>Risk:</b>{road['risk_level']}<br>

        <b>Traffic:</b>{road['traffic_status']}

        """



        folium.CircleMarker(

            location=[

                road["latitude"],

                road["longitude"]

            ],


            radius=7,

            color=color,

            fill=True,

            popup=popup


        ).add_to(dashboard)





    # =============================
    # TRAFFIC SIGNALS
    # =============================


    signals = load_json(

        "outputs/traffic_signals.json"

    )


    for signal in signals:


        folium.Marker(

            [

                signal["latitude"],

                signal["longitude"]

            ],


            popup="Traffic Signal 🚦",


            icon=folium.Icon(

                color="red",

                icon="info-sign"

            )


        ).add_to(dashboard)






    # =============================
    # FINAL ARCHITECT INSIGHT
    # =============================


    report = load_json(

        "outputs/final_architect_report.json"

    )



    if report:


        insight = f"""

        <h3>Final Circulation Insight</h3>


        <b>Recommended:</b><br>

        {report['recommended_entry']}


        <br><br>


        <b>Avoid:</b><br>

        {report['avoid_entry']}

        """



        folium.Marker(

            [site_lat, site_lon],


            popup=insight,


            icon=folium.Icon(

                color="green",

                icon="ok-sign"

            )


        ).add_to(dashboard)





    os.makedirs(

        "outputs",

        exist_ok=True

    )



    dashboard.save(

        "outputs/architect_dashboard.html"

    )



    print(

        "Saved outputs/architect_dashboard.html"

    )






if __name__ == "__main__":

    generate_dashboard()