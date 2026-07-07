import json
import os



def save_report(data):


    os.makedirs(
        "outputs",
        exist_ok=True
    )


    file_path = (
        "outputs/traffic_report.json"
    )


    with open(
        file_path,
        "w"
    ) as file:


        json.dump(
            data,
            file,
            indent=4
        )



    print(
        "\nReport saved:",
        file_path
    )