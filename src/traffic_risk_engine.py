def calculate_risk(
        road_type,
        traffic_status,
        connected_roads
):


    risk_score = 0


    # Traffic congestion impact

    if traffic_status == "HIGH TRAFFIC":

        risk_score += 50


    elif traffic_status == "MEDIUM TRAFFIC":

        risk_score += 30


    else:

        risk_score += 10



    # Road importance impact

    if road_type in [

        "primary",
        "trunk",
        "motorway"

    ]:

        risk_score += 30


    elif road_type in [

        "secondary",
        "tertiary"

    ]:

        risk_score += 20


    else:

        risk_score += 10



    # Intersection complexity impact

    if connected_roads >= 5:

        risk_score += 20


    elif connected_roads >= 3:

        risk_score += 10



    # Risk category

    if risk_score >= 70:

        risk_level = "HIGH RISK"


    elif risk_score >= 40:

        risk_level = "MEDIUM RISK"


    else:

        risk_level = "LOW RISK"



    return {

        "score": risk_score,

        "level": risk_level

    }