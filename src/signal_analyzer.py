import osmnx as ox
import json
import os



def analyze_traffic_signals():


    print(
        "\n===== TRAFFIC SIGNAL ANALYSIS ====="
    )


    # Test site coordinate (REVA area)
    latitude = 13.1168

    longitude = 77.6347


    radius = 1000



    tags = {

        "highway": "traffic_signals"

    }



    signals = ox.features_from_point(

        (
            latitude,
            longitude
        ),

        tags,

        dist=radius

    )



    signal_data = []



    for index, signal in signals.iterrows():


        geometry = signal.geometry



        # some signals are points
        if geometry.geom_type == "Point":


            signal_lat = geometry.y

            signal_lon = geometry.x


        else:


            center = geometry.centroid

            signal_lat = center.y

            signal_lon = center.x




        data = {


            "latitude": signal_lat,

            "longitude": signal_lon,

            "type": "traffic_signal"

        }



        signal_data.append(
            data
        )



        print(

            "Signal found:",

            signal_lat,

            signal_lon

        )




    os.makedirs(

        "outputs",

        exist_ok=True

    )



    with open(

        "outputs/traffic_signals.json",

        "w"

    ) as file:


        json.dump(

            signal_data,

            file,

            indent=4

        )



    print(

        "\nTotal Signals Found:",

        len(signal_data)

    )


    print(

        "Saved: outputs/traffic_signals.json"

    )





if __name__ == "__main__":


    analyze_traffic_signals()