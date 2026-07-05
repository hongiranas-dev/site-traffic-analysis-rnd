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

        degree = graph.degree(node)

        connected_edges = graph.edges(node, data=True)

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


        if degree >= 4 and has_major_road:
            conflict_points[node] = degree


    return conflict_points



def create_conflict_map(graph):

    nodes = graph.nodes

    conflict_points = find_conflict_points(graph)

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


    for node_id, degree in conflict_points.items():

        latitude = nodes[node_id]["y"]
        longitude = nodes[node_id]["x"]


        folium.Marker(
            location=[
                latitude,
                longitude
            ],

            popup=f"""
            Node ID: {node_id}
            Connected Roads: {degree}
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

    print("Starting conflict analysis...")

    road_graph = extract_roads()

    create_conflict_map(
        road_graph
    )