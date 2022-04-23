import json
import requests as req
import base64


def get_token(self):
    # Step 1. Setting AuthOption
    json_file = open("auth.json")
    auth = json.load(json_file)
    auth_data = "{}:{}".format(
        auth['CLIENT_ID'],
        auth['CLIENT_SECRET']
    )
    authorization = "Basic " + \
        base64.b64encode(auth_data.encode('ascii')).decode("ascii")

    # Step 2. Setting Request Datas
    token_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": authorization
    }
    data = {
        "grant_type": "client_credentials"
    }

    # Step 3. Request
    res = req.post(token_url, data=data, headers=headers)
    token = res.json()['access_token']

    self.token = token
