#traffic insights
from osm_extractor import extract_roads


def find_conflict_points(graph):

    degrees = dict(graph.degree())

    conflict_points = {
        node: degree
        for node, degree in degrees.items()
        if degree >= 4
    }


    print("\nPossible Traffic Conflict Points:")

    print("Total:", len(conflict_points))


    for node, degree in list(conflict_points.items())[:10]:

        print(
            "Node:",
            node, # the node number is given by osm
            "Connected Roads:",
            degree
        )


if __name__ == "__main__":

    road_graph = extract_roads()

    find_conflict_points(road_graph)