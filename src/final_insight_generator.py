import json
import os
from live_traffic_summary import build_live_traffic_summary



def load_json(path):

    if os.path.exists(path):

        with open(path, "r") as file:

            return json.load(file)

    return []




def risk_value(level):

    values = {

        "LOW RISK": 1,

        "MEDIUM RISK": 2,

        "HIGH RISK": 3

    }


    return values.get(level, 2)





def generate_report():


    print(
        "\n===== FINAL SITE CIRCULATION ANALYSIS ====="
    )


    directions = load_json(
        "outputs/direction_analysis.json"
    )


    zoning = load_json(
        "outputs/zoning_analysis.json"
    )


    signals = load_json(
        "outputs/traffic_signals.json"
    )


    pedestrian = load_json(
        "outputs/pedestrian_analysis.json"
    )

    live_traffic = build_live_traffic_summary()



    # sort roads safest -> riskiest

    ranked_roads = sorted(

        directions,

        key=lambda x: risk_value(

            x["risk_level"]

        )

    )



    best_road = ranked_roads[0]

    worst_road = ranked_roads[-1]




    recommended_entry = (

        best_road["direction"]

        + " side via "

        + best_road["road_name"]

    )



    avoid_entry = (

        worst_road["direction"]

        + " side via "

        + worst_road["road_name"]

    )




    reasons = [


        worst_road["road_name"]

        + " has comparatively higher circulation risk"

    ]



    if zoning:


        reasons.append(

            zoning["zone_type"]

            + " land-use increases movement demand"

        )



    if signals:


        reasons.append(

            str(len(signals))

            + " nearby signals may create vehicle queues"

        )



    if pedestrian:


        reasons.append(

            pedestrian["pedestrian_level"]

            + " requires pedestrian planning"

        )

    tomtom = live_traffic["tomtom"]
    if tomtom["snapshot"].get("available"):
        freshness = "fresh" if tomtom["snapshot"].get("fresh") else "stale"
        reasons.append(
            "TomTom "
            + freshness
            + " snapshot: "
            + str(tomtom["roads_analyzed"])
            + " roads, average congestion index "
            + str(tomtom["average_congestion_index"])
        )

    if live_traffic["iudx"]["bmtc_live_positions"]["discovered"]:
        bmtc = live_traffic["iudx"]["bmtc_live_positions"]
        if bmtc["available"]:
            reasons.append(
                "IUDX BMTC live snapshot: "
                + str(bmtc["vehicle_count"])
                + " buses displayed as blue points on the dashboard"
            )
        else:
            reasons.append(
                "IUDX BMTC live-position feed discovered; awaiting authenticated collection"
            )




    print(

        "\nRecommended Entry:"

    )


    print(

        recommended_entry

    )



    print(

        "\nAvoid:"

    )


    print(

        avoid_entry

    )



    print(

        "\nReason:"

    )


    for r in reasons:

        print(
            "-",
            r
        )




    print(

        "\nSuggested:"

    )


    suggestions = [

        "Separate pedestrian and vehicle access",

        "Provide safe pedestrian crossing zones",

        "Avoid main entry near high movement roads",

        "Design access considering peak hour traffic"

    ]



    for s in suggestions:


        print(

            "-",

            s

        )




    final = {


        "recommended_entry": recommended_entry,


        "avoid_entry": avoid_entry,


        "reasons": reasons,


        "suggestions": suggestions,

        "live_traffic": live_traffic

    }



    with open(

        "outputs/final_architect_report.json",

        "w"

    ) as file:


        json.dump(

            final,

            file,

            indent=4

        )




    print(

        "\nSaved outputs/final_architect_report.json"

    )





if __name__ == "__main__":


    generate_report()
