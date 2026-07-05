import osmnx as ox

from osm_extractor import extract_roads


def estimate_capacity(road_type):

    if isinstance(road_type, list):
        road_type = road_type[0]


    capacity_map = {

        "motorway": "VERY HIGH",
        "trunk": "VERY HIGH",

        "primary": "HIGH",

        "secondary": "MEDIUM",
        "tertiary": "MEDIUM",

        "residential": "LOW",
        "service": "LOW",
        "living_street": "LOW"
    }


    return capacity_map.get(
        road_type,
        "UNKNOWN"
    )



def analyze_capacity(graph):

    nodes, edges = ox.graph_to_gdfs(graph)


    print(
        "\n===== ROAD CAPACITY ANALYSIS ====="
    )


    total_roads = 0

    high_capacity = 0
    medium_capacity = 0
    low_capacity = 0


    for index, road in edges.iterrows():


        # road name
        road_name = road.get(
            "name",
            "Unnamed Road"
        )


        # road category
        road_type = road.get(
            "highway",
            "unknown"
        )


        # road length
        length = road.get(
            "length",
            0
        )


        # capacity
        capacity = estimate_capacity(
            road_type
        )


        total_roads += 1


        if capacity == "HIGH" or capacity == "VERY HIGH":
            high_capacity += 1

        elif capacity == "MEDIUM":
            medium_capacity += 1

        elif capacity == "LOW":
            low_capacity += 1



        print(
            "\n----------------------"
        )

        print(
            "Road Name:",
            road_name
        )

        print(
            "Road Type:",
            road_type
        )

        print(
            "Length:",
            round(length,2),
            "meters"
        )

        print(
            "Estimated Capacity:",
            capacity
        )



    print(
        "\n===== SUMMARY ====="
    )

    print(
        "Total Roads:",
        total_roads
    )

    print(
        "High Capacity Roads:",
        high_capacity
    )

    print(
        "Medium Capacity Roads:",
        medium_capacity
    )

    print(
        "Low Capacity Roads:",
        low_capacity
    )



if __name__ == "__main__":


    print(
        "Starting road capacity analysis..."
    )


    road_graph = extract_roads()


    analyze_capacity(
        road_graph
    )