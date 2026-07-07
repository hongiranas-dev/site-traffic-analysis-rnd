import osmnx as ox
import json
import os



def analyze_zone():


    print(
        "\n===== CONTEXTUAL ZONING ANALYSIS ====="
    )


    # Test site coordinate (REVA)
    latitude = 13.1168

    longitude = 77.6347


    radius = 1000



    tags = {

        "building": True,

        "amenity": True,

        "shop": True,

        "office": True

    }



    features = ox.features_from_point(

        (
            latitude,
            longitude
        ),

        tags,

        dist=radius

    )



    residential_score = 0

    commercial_score = 0



    for index, feature in features.iterrows():


        building = feature.get(
            "building",
            ""
        )


        amenity = feature.get(
            "amenity",
            ""
        )


        shop = feature.get(
            "shop",
            ""
        )


        office = feature.get(
            "office",
            ""
        )



        # Residential indicators

        if building in [

            "residential",
            "apartments",
            "house"

        ]:


            residential_score += 1




        # Commercial indicators

        if (

            shop != ""

            or

            office != ""

            or

            amenity in [

                "restaurant",
                "cafe",
                "bank",
                "school",
                "college",
                "hospital"

            ]

        ):


            commercial_score += 1





    if commercial_score > residential_score:


        zone_type = "COMMERCIAL"


        traffic_multiplier = 1.5



    elif residential_score > commercial_score:


        zone_type = "RESIDENTIAL"


        traffic_multiplier = 1.2



    else:


        zone_type = "MIXED"


        traffic_multiplier = 1.3





    result = {


        "zone_type": zone_type,


        "residential_score": residential_score,


        "commercial_score": commercial_score,


        "traffic_multiplier": traffic_multiplier

    }



    os.makedirs(

        "outputs",

        exist_ok=True

    )



    with open(

        "outputs/zoning_analysis.json",

        "w"

    ) as file:


        json.dump(

            result,

            file,

            indent=4

        )




    print(

        "Zone Type:",

        zone_type

    )


    print(

        "Residential Score:",

        residential_score

    )


    print(

        "Commercial Score:",

        commercial_score

    )


    print(

        "Traffic Multiplier:",

        traffic_multiplier

    )



    print(

        "\nSaved: outputs/zoning_analysis.json"

    )




if __name__ == "__main__":


    analyze_zone()