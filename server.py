from flask import Flask
from flask import request
from requests import get
import json

app = Flask(__name__)


@app.route("/")
def returnCoordinates():
    ips = ['2.2.2.2', '8.8.8.8', '5.5.5.5']
    placesObj = {
        "places": []
    }
    for ip in ips:
        loc = get(f'https://ipapi.co/{ip}/json/')
        loc = loc.json()
        placesObj["places"].append({
            "coords": {
                "lat": loc["latitude"],
                "lng": loc["longitude"]
            },
            "text": loc["city"]
        })

    return json.dumps(placesObj)


# if __name__ == "__main__":
#     app.debug = True
#     app.run()
