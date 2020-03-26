from flask import Flask
from flask import request
from requests import post
import json

app = Flask(__name__)


@app.route("/")
def returnCoordinates():
    ips = ['2.2.2.2', '8.8.8.8', '5.5.5.5']
    res = post(url='http://ip-api.com/batch', json=ips).json()
    output = {
        "places": []
    }
    for loc in res:
        place = {
            "coords": {
                "lat": loc["lon"],
                "lng": loc["lon"]
            },
            "text": loc["city"]
        }
        output["places"].append(place)
    return json.dumps(output)


if __name__ == "__main__":
    app.debug = True
    app.run()
