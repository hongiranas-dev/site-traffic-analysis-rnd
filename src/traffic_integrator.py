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

    print("\n===== ARCHITECT TRAFFIC INSIGHT REPORT =====")

    # Group OSM segments by road name and road type
    road_groups = {}

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

        if str(road_name) == "nan" or not road_name:
            road_name = "Unnamed Road"

        # Keep unnamed roads separate
        key = (
            str(road_name),
            str(road_type)
        )

        if key not in road_groups:
            road_groups[key] = []

        road_groups[key].append(
            (index, road)
        )

    # Analyze each named physical road once
    for (road_name, road_type), segments in road_groups.items():

        # Use the longest segment as the representative
        representative_index, representative_road = max(
            segments,
            key=lambda item: item[1].get(
                "length",
                0
            )
        )

        geometry = representative_road["geometry"]

        midpoint = geometry.interpolate(
            0.5,
            normalized=True
        )

        latitude = midpoint.y
        longitude = midpoint.x

        # One TomTom lookup per road group
        traffic = get_traffic_data(
            latitude,
            longitude
        )

        # Use the representative segment's start node
        start_node = representative_index[0]

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

            "architect_insight": insight,

            "segments_grouped": len(segments)

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
            "Road type:",
            road_type
        )

        print(
            "Segments grouped:",
            len(segments)
        )

        print(
            "Risk:",
            risk["level"]
        )

        print(
            "Score:",
            risk["score"]
        )

    save_report(
        report_data
    )

    print("\nCompleted")

    print(
        "Physical roads analyzed:",
        len(report_data)
    )


if __name__ == "__main__":

    road_graph = extract_roads()

    analyze_site_traffic(
        road_graph
    )