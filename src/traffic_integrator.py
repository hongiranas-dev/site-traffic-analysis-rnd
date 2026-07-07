import osmnx as ox

from osm_extractor import extract_roads
from traffic_api import get_traffic_data
from traffic_risk_engine import calculate_risk
from report_generator import save_report


def architect_recommendation(risk_level):

    if risk_level == "HIGH RISK":
        return "Avoid main entry/exit here. High congestion possibility."

    elif risk_level == "MEDIUM RISK":
        return "Usable road but requires traffic planning."

    else:
        return "Suitable zone for smoother vehicle circulation."



def analyze_site_traffic(graph):

    nodes, edges = ox.graph_to_gdfs(graph)


    important_roads = [
        "primary",
        "secondary",
        "tertiary",
        "trunk",
        "motorway"
    ]


    report_data = []

    analyzed_count = 0


    print("\n===== ARCHITECT TRAFFIC INSIGHT REPORT =====")


    for index, road in edges.iterrows():


        road_type = road.get(
            "highway",
            "unknown"
        )


        if isinstance(road_type, list):
            road_type = road_type[0]


        if road_type not in important_roads:
            continue



        road_name = road.get(
            "name",
            "Unnamed Road"
        )


        if str(road_name) == "nan":
            road_name = "Unnamed Road"



        geometry = road["geometry"]


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



        start_node = index[0]


        connected_roads = graph.degree(
            start_node
        )



        risk = calculate_risk(
            road_type,
            traffic["status"],
            connected_roads
        )


        insight = architect_recommendation(
            risk["level"]
        )



        road_report = {

            "road_name": road_name,

            "road_type": road_type,

            "latitude": latitude,

            "longitude": longitude,

            "connected_roads": connected_roads,

            "current_speed": traffic["current_speed"],

            "free_flow_speed": traffic["free_speed"],

            "traffic_status": traffic["status"],

            "risk_score": risk["score"],

            "risk_level": risk["level"],

            "architect_insight": insight

        }



        report_data.append(
            road_report
        )



        print("\n------------------------")

        print(
            "Road:",
            road_name
        )

        print(
            "Risk:",
            risk["level"]
        )

        print(
            "Score:",
            risk["score"]
        )



        analyzed_count += 1


        if analyzed_count == 30:
            break



    save_report(
        report_data
    )


    print("\nCompleted")

    print(
        "Roads analyzed:",
        analyzed_count
    )




if __name__ == "__main__":


    road_graph = extract_roads()


    analyze_site_traffic(
        road_graph
    )