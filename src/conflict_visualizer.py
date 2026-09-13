import folium

from osm_extractor import extract_roads


def find_conflict_points(graph):

    conflict_points = {}

    important_roads = [
        "primary",
        "secondary",
        "tertiary",
        "trunk",
        "motorway"
    ]

    for node in graph.nodes:

        connected_edges = graph.edges(
            node,
            data=True
        )

        connected_roads = set()
        has_major_road = False

        for edge in connected_edges:

            road_type = edge[2].get(
                "highway",
                ""
            )

            if isinstance(road_type, list):
                road_type = road_type[0]

            if road_type in important_roads:

                has_major_road = True

                road_name = edge[2].get(
                    "name",
                    "Unnamed Road"
                )

                if isinstance(road_name, list):
                    road_name = road_name[0]

                if (
                    not road_name
                    or str(road_name).lower() == "nan"
                ):
                    road_name = "Unnamed Road"

                connected_roads.add(
                    str(road_name)
                )

        # Count distinct roads rather than raw OSM edges
        road_count = len(connected_roads)

        if road_count >= 3 and has_major_road:

            conflict_points[node] = {
                "road_count": road_count,
                "roads": sorted(connected_roads)
            }

    return conflict_points


def create_conflict_map(graph):

    nodes = graph.nodes

    conflict_points = find_conflict_points(
        graph
    )

    first_node = list(nodes)[0]

    center_lat = nodes[first_node]["y"]
    center_lon = nodes[first_node]["x"]

    m = folium.Map(
        location=[
            center_lat,
            center_lon
        ],
        zoom_start=15
    )

    for node_id, conflict_data in conflict_points.items():

        latitude = nodes[node_id]["y"]
        longitude = nodes[node_id]["x"]

        road_count = conflict_data[
            "road_count"
        ]

        roads = conflict_data[
            "roads"
        ]

        road_list = "<br>".join(
            roads
        )

        folium.Marker(

            location=[
                latitude,
                longitude
            ],

            popup=f"""
            <b>Junction Conflict Point</b><br>
            Node ID: {node_id}<br>
            Distinct Roads: {road_count}<br>
            <br>
            <b>Connected Roads:</b><br>
            {road_list}
            """

        ).add_to(m)

    m.save(
        "data/conflict_points.html"
    )

    print(
        "Conflict map created successfully"
    )

    print(
        "Total conflict points:",
        len(conflict_points)
    )


if __name__ == "__main__":

    print(
        "Starting conflict analysis..."
    )

    road_graph = extract_roads()

    create_conflict_map(
        road_graph
    )