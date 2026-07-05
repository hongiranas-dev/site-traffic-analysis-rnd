import osmnx as ox
import folium


# Test site location (REVA University)
LATITUDE = 13.1168
LONGITUDE = 77.6347
RADIUS = 1000  # meters


def extract_roads():

    print("Downloading road network...")

    # Get roads within 1km
    graph = ox.graph_from_point(
        (LATITUDE, LONGITUDE),
        dist=RADIUS,
        network_type="drive"
    )

    print("Download complete!")

    return graph


def analyze_roads(graph):

    # Convert graph into tables
    nodes, edges = ox.graph_to_gdfs(graph)

    print("\n--- ANALYSIS ---")
    print("Intersections:", len(nodes))  
    print("Road segments:", len(edges))

    print("\nRoad Types:")
    print(edges["highway"].value_counts()) #its classifys impo roads

    return nodes, edges


def create_map(edges):

    m = folium.Map(
        location=[LATITUDE, LONGITUDE],
        zoom_start=15
    )

    for _, road in edges.iterrows():
        coords = [
            (lat, lon)
            for lon, lat in road.geometry.coords
        ]

        folium.PolyLine(coords).add_to(m)

    m.save("data/road_network.html")

    print("\nMap saved: data/road_network.html")


if __name__ == "__main__":

    road_graph = extract_roads()

    nodes, edges = analyze_roads(road_graph)

    create_map(edges)

