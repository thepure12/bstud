from bottle_suite import Resource
import requests
import toml
import os

try:
    config = toml.load("config.toml")
    BITLY_URL = config["bitly_url"]
    API_TOKEN = config["bitly_token"]
    BITLY_GROUP = config["bitly_group"]
except:
    BITLY_URL = os.environ.get("BITLY_URL")
    API_TOKEN = os.environ.get("BITLY_API_TOKEN")
    BITLY_GROUP = os.environ.get("BITLY_GROUP")
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}


class ShareURL(Resource):
    def options(self):
        pass

    def post(self, url=""):
        long_url = url
        if long_url:
            print(long_url)
            res = requests.post(
                BITLY_URL,
                json={
                    "group_guid": BITLY_GROUP,
                    "domain": "bit.ly",
                    "long_url": long_url,
                },
                headers=HEADERS,
            )
            if res.status_code == 200:
                return {"link": res.json()["link"]}
            print(res.json())
        return {"link": ""}
