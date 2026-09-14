import osmnx as ox
import json
import os

from config import SITE_LAT, SITE_LON, SEARCH_RADIUS


def analyze_zone():

    print(
        "\n===== CONTEXTUAL ZONING ANALYSIS ====="
    )

    tags = {
        "building": True,
        "amenity": True,
        "shop": True,
        "office": True
    }

    features = ox.features_from_point(
        (
            SITE_LAT,
            SITE_LON
        ),
        tags,
        dist=SEARCH_RADIUS
    )

    residential_score = 0
    commercial_score = 0
    institutional_score = 0

    counted_features = set()

    for index, feature in features.iterrows():

        feature_id = str(index)

        if feature_id in counted_features:
            continue

        counted_features.add(feature_id)

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

        # Institutional indicators
        if amenity in [
            "school",
            "college",
            "university",
            "hospital",
            "clinic",
            "kindergarten",
            "research_institute"
        ]:
            institutional_score += 1
            continue

        # Residential indicators
        if building in [
            "residential",
            "apartments",
            "house",
            "detached",
            "semidetached_house"
        ]:
            residential_score += 1
            continue

        # Plain buildings are treated as probable residential
        if building not in [
            "",
            "yes",
            None
        ]:
            residential_score += 1
            continue

        # Commercial indicators
        if (
            shop != ""
            or office != ""
            or amenity in [
                "restaurant",
                "cafe",
                "bank",
                "fast_food",
                "marketplace"
            ]
        ):
            commercial_score += 1

    total_score = (
        residential_score
        + commercial_score
        + institutional_score
    )

    # Determine dominant land-use category
    if total_score == 0:

        zone_type = "UNKNOWN"
        traffic_multiplier = 1.0

    else:

        residential_ratio = (
            residential_score / total_score
        )

        commercial_ratio = (
            commercial_score / total_score
        )

        institutional_ratio = (
            institutional_score / total_score
        )

        if (
            institutional_ratio >= 0.40
            and institutional_score >= commercial_score
            and institutional_score >= residential_score
        ):

            zone_type = "INSTITUTIONAL"
            traffic_multiplier = 1.4

        elif (
            residential_ratio >= 0.40
            and commercial_ratio <= 0.60
        ):

            zone_type = "RESIDENTIAL"
            traffic_multiplier = 1.2

        elif (
            commercial_ratio >= 0.40
            and residential_ratio <= 0.60
        ):

            zone_type = "COMMERCIAL"
            traffic_multiplier = 1.5

        else:

            zone_type = "MIXED"
            traffic_multiplier = 1.3

    result = {

        "zone_type": zone_type,

        "residential_score": residential_score,

        "commercial_score": commercial_score,

        "institutional_score": institutional_score,

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
        "Institutional Score:",
        institutional_score
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

