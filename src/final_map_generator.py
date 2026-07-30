import json
import folium
import os
from branca.element import Element
from map_provider import create_map
from live_traffic_summary import build_live_traffic_summary



def create_final_map():


    with open(
        "outputs/final_architect_report.json",
        "r"
    ) as file:


        report = json.load(file)



    site_lat = 13.1168

    site_lon = 77.6347



    final_map = create_map([site_lat, site_lon], zoom_start=15)
    live_traffic = build_live_traffic_summary()



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





    tomtom = live_traffic["tomtom"]
    bmtc = live_traffic["iudx"]["bmtc_live_positions"]
    key_reason = report["reasons"][0] if report.get("reasons") else "No risk reason available"
    key_suggestion = report["suggestions"][0] if report.get("suggestions") else "No design suggestion available"
    bmtc_label = (
        f"{bmtc['vehicle_count']} live buses" if bmtc["available"] else "Awaiting BMTC snapshot"
    )
    summary_card = f"""
    <div style="position: fixed; top: 12px; right: 12px; z-index: 1000;
                width: 280px; background: white; border: 2px solid #555;
                border-radius: 7px; padding: 12px; font-size: 13px; line-height: 1.35;">
      <b style="font-size: 15px;">Site Access Summary</b><br><br>
      <b>Recommended:</b> {report['recommended_entry']}<br>
      <b>Avoid:</b> {report['avoid_entry']}<br><br>
      <b>Live traffic:</b> TomTom index {tomtom['average_congestion_index']}<br>
      <b>BMTC / IUDX:</b> {bmtc_label}<br><br>
      <b>Key risk:</b> {key_reason}<br><br>
      <b>Design action:</b> {key_suggestion}
    </div>
    """
    final_map.get_root().html.add_child(Element(summary_card))




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
