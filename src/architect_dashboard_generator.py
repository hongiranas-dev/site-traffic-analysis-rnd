import folium
import json
import os
from branca.element import Element
from map_provider import create_map
from live_traffic_summary import build_live_traffic_summary



def load_json(path):

    if os.path.exists(path):

        with open(path, "r") as file:

            return json.load(file)

    return []


def bus_coordinates(position):
    location = position.get("location", {})
    if isinstance(location, dict):
        coordinates = location.get("coordinates")
        if isinstance(coordinates, list) and len(coordinates) >= 2:
            return coordinates[1], coordinates[0]

    coordinates = position.get("location.coordinates")
    if isinstance(coordinates, list) and len(coordinates) >= 2:
        return coordinates[1], coordinates[0]

    return None


def load_bmtc_positions():
    snapshot = load_json("outputs/iudx_live_bmtc_positions.json")
    if isinstance(snapshot, list):
        return snapshot
    return snapshot.get("vehicle_positions", [])




def generate_dashboard():


    print("\n===== GENERATING ARCHITECT DASHBOARD =====")


    site_lat = 13.1168
    site_lon = 77.6347


    dashboard = create_map([site_lat, site_lon], zoom_start=15)
    live_traffic = build_live_traffic_summary()



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



        congestion_index = (
            road["free_flow_speed"] / road["current_speed"]
            if road["current_speed"] > 0
            else None
        )
        popup = f"""

        <b>Road:</b>{road['road_name']}<br>

        <b>Risk:</b>{road['risk_level']}<br>

        <b>Traffic:</b>{road['traffic_status']}

        <br><b>TomTom speed:</b> {road['current_speed']} km/h

        <br><b>Free-flow:</b> {road['free_flow_speed']} km/h

        <br><b>Congestion index:</b> {congestion_index:.2f}

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

    tomtom = live_traffic["tomtom"]
    snapshot = tomtom["snapshot"]
    snapshot_label = (
        f"{snapshot['age_minutes']} minutes ago ({'fresh' if snapshot['fresh'] else 'stale'})"
        if snapshot.get("available")
        else snapshot["message"]
    )
    iudx_bmtc = live_traffic["iudx"]["bmtc_live_positions"]
    iudx_events = live_traffic["iudx"]["traffic_events"]
    source_panel = f"""
    <div style="position: fixed; top: 12px; right: 12px; z-index: 1000;
                background: white; border: 2px solid #555; border-radius: 6px;
                padding: 12px; max-width: 310px; font-size: 13px;">
      <b>Live Traffic Sources</b><br><br>
      <b>TomTom (primary)</b><br>
      Snapshot: {snapshot_label}<br>
      Roads: {tomtom['roads_analyzed']}<br>
      Average speed: {tomtom['average_current_speed_kmph']} km/h<br>
      Average congestion index: {tomtom['average_congestion_index']}<br><br>
      <b>IUDX BMTC</b><br>
      {iudx_bmtc['status']}<br><br>
      <b>IUDX Traffic Events</b><br>
      {iudx_events['status']}
    </div>
    """
    dashboard.get_root().html.add_child(Element(source_panel))

    for position in load_bmtc_positions()[:200]:
        coordinates = bus_coordinates(position)
        if not coordinates:
            continue

        vehicle = position.get("vehicle", {})
        trip = position.get("trip", {})
        vehicle_id = vehicle.get("id", position.get("vehicle.id", "Unknown"))
        route_id = trip.get("route_id", position.get("trip.route_id", "Unknown"))
        folium.CircleMarker(
            location=coordinates,
            radius=3,
            color="blue",
            fill=True,
            fill_opacity=0.8,
            popup=f"BMTC bus: {vehicle_id}<br>Route: {route_id}",
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

        # =============================
    # FASTAPI CONNECTION
    # =============================

    api_script = """
    <script>

    async function loadTrafficFromAPI() {
        try {
            const response = await fetch("/api/traffic");

            if (!response.ok) {
                throw new Error("Traffic API failed");
            }

            const traffic = await response.json();

            console.log("Traffic data received from FastAPI:", traffic);

        } catch (error) {
            console.error("Traffic API error:", error);
        }
    }


    async function loadDirectionsFromAPI() {
        try {
            const response = await fetch("/api/directions");

            if (!response.ok) {
                throw new Error("Directions API failed");
            }

            const directions = await response.json();

            console.log("Direction data received from FastAPI:", directions);

        } catch (error) {
            console.error("Directions API error:", error);
        }
    }


    async function loadSignalsFromAPI() {
        try {
            const response = await fetch("/api/signals");

            if (!response.ok) {
                throw new Error("Signals API failed");
            }

            const signals = await response.json();

            console.log("Signal data received from FastAPI:", signals);

        } catch (error) {
            console.error("Signals API error:", error);
        }
    }


    async function loadZoningFromAPI() {
        try {
            const response = await fetch("/api/zoning");

            if (!response.ok) {
                throw new Error("Zoning API failed");
            }

            const zoning = await response.json();

            console.log("Zoning data received from FastAPI:", zoning);

        } catch (error) {
            console.error("Zoning API error:", error);
        }
    }


    async function loadPedestrianFromAPI() {
        try {
            const response = await fetch("/api/pedestrian");

            if (!response.ok) {
                throw new Error("Pedestrian API failed");
            }

            const pedestrian = await response.json();

            console.log("Pedestrian data received from FastAPI:", pedestrian);

        } catch (error) {
            console.error("Pedestrian API error:", error);
        }
    }


    async function loadInsightsFromAPI() {
        try {
            const response = await fetch("/api/insights");

            if (!response.ok) {
                throw new Error("Insights API failed");
            }

            const insights = await response.json();

            console.log("Insights received from FastAPI:", insights);

        } catch (error) {
            console.error("Insights API error:", error);
        }
    }


    // Load all backend data
    loadTrafficFromAPI();
    loadDirectionsFromAPI();
    loadSignalsFromAPI();
    loadZoningFromAPI();
    loadPedestrianFromAPI();
    loadInsightsFromAPI();

    </script>
    """

    dashboard.get_root().html.add_child(
        Element(api_script)
    )

    dashboard.save(

        "outputs/architect_dashboard.html"

    )



    print(

        "Saved outputs/architect_dashboard.html"

    )






if __name__ == "__main__":

    generate_dashboard()
