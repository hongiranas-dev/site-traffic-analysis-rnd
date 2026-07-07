import json
import folium
import os



def create_final_map():


    with open(
        "outputs/final_architect_report.json",
        "r"
    ) as file:


        report = json.load(file)



    site_lat = 13.1168

    site_lon = 77.6347



    final_map = folium.Map(

        location=[

            site_lat,

            site_lon

        ],

        zoom_start=15

    )



    # Site marker

    folium.Marker(

        location=[

            site_lat,

            site_lon

        ],


        popup="Project Site",


        icon=folium.Icon(

            color="blue",

            icon="home"

        )

    ).add_to(

        final_map

    )





    insight = f"""

    <h3>Site Circulation Report</h3>


    <b>Recommended Entry:</b><br>

    {report['recommended_entry']}

    <br><br>


    <b>Avoid Entry:</b><br>

    {report['avoid_entry']}


    <br><br>


    <b>Reasons:</b><br>

    {"<br>".join(report['reasons'])}


    <br><br>


    <b>Suggestions:</b><br>

    {"<br>".join(report['suggestions'])}

    """




    folium.Marker(

        location=[

            site_lat,

            site_lon

        ],


        popup=insight,


        icon=folium.Icon(

            color="green",

            icon="info-sign"

        )

    ).add_to(

        final_map

    )




    os.makedirs(

        "outputs",

        exist_ok=True

    )



    final_map.save(

        "outputs/final_circulation_map.html"

    )



    print(

        "Saved outputs/final_circulation_map.html"

    )






if __name__ == "__main__":


    create_final_map()