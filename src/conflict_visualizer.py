import folium

from osm_extractor import extract_roads


def get_junction_complexity(graph, node):

    degree = graph.degree(node)

    if degree >= 5:
        return "HIGH", degree

    elif degree >= 3:
        return "MEDIUM", degree

    else:
        return "LOW", degree


def find_conflict_points(graph):

    conflict_points = {}

    for node in graph.nodes:

        complexity, degree = get_junction_complexity(
            graph,
            node
        )

        if degree >= 3:

            conflict_points[node] = {
                "degree": degree,
                "complexity": complexity
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

    for node_id, data in conflict_points.items():

        latitude = nodes[node_id]["y"]
        longitude = nodes[node_id]["x"]

        folium.Marker(

            location=[
                latitude,
                longitude
            ],

            popup=f"""
            <b>Junction Conflict Point</b><br>
            Connected Roads: {data["degree"]}<br>
            Complexity: {data["complexity"]}
            """

        ).add_to(m)

    m.save(
        "data/conflict_points.html"
    )

    print(
        "\n===== JUNCTION ANALYSIS ====="
    )

    print(
        "Conflict points:",
        len(conflict_points)
    )

    print(
        "Conflict map created successfully"
    )


if __name__ == "__main__":

    print(
        "Starting conflict analysis..."
    )

    road_graph = extract_roads()

    create_conflict_map(
        road_graph
    )