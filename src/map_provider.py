"""Create Folium maps with an optional MapTiler basemap."""

import os

import folium


def create_map(location, zoom_start=15):
    maptiler_key = os.getenv("MAPTILER_API_KEY")
    if not maptiler_key:
        return folium.Map(location=location, zoom_start=zoom_start)

    traffic_map = folium.Map(location=location, zoom_start=zoom_start, tiles=None)
    folium.TileLayer(
        tiles=(
            "https://api.maptiler.com/maps/streets-v2/"
            "{z}/{x}/{y}.png?key=" + maptiler_key
        ),
        attr="&copy; MapTiler &copy; OpenStreetMap contributors",
        name="MapTiler Streets",
        overlay=False,
        control=False,
    ).add_to(traffic_map)
    return traffic_map
