from flask import Flask
from flask import request
from flask_cors import CORS
from requests import get, post
from bs4 import BeautifulSoup as bs
import json
import re

app = Flask(__name__)
cors = CORS(app)


def parse_page(url):
    ip_list = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    r = get(url, headers=headers)
    if(r.status_code == 200):
        soup = bs(r.content, "html.parser")
        history = soup.find(id="pagehistory")
        history_list = history.find_all('li')
        for list_item in history_list:
            history = list_item.find(
                "span", {"class": "history-user"}).get_text().strip()
            ip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', history)
            if ip:
                ip_list.append(ip[0])
    return ip_list


@app.route("/")
def returnCoordinates():
    url = request.args.get('url')
    if url is None or len(url) == 0:
        return ''
    url += '&offset=&limit=100&action=history'
    ips = parse_page(url)
    res = post(url='http://ip-api.com/batch', json=ips).json()
    output = {
        "places": []
    }
    for loc in res:
        place = {
            "coords": {
                "lat": loc["lat"],
                "lng": loc["lon"]
            },
            "text": loc["city"]
        }
        output["places"].append(place)
    return json.dumps(output)


# if __name__ == "__main__":
#     app.debug = True
#     app.run()
