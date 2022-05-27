import base64
import pandas as pd
import requests as req
from urllib.parse import urlencode
from functools import reduce


def get_track(self, id):
    search_uri = "https://api.spotify.com/v1/tracks/{}".format(id)

    query = urlencode({
        "market": "KR"
    })

    headers = {
        "authorization": "Bearer {}".format(self.token)
    }

    res = req.get("{}?{}".format(search_uri, query), headers=headers)

    item = res.json()

    _id = item["id"]
    _name = item["name"]
    album = item['album']
    images = album["images"]

    if len(images) == 0:
        _image = ""
    else:
        _image = images[0]['url']

    artist_list = album['artists']
    artists = reduce(
        lambda acc, cur: cur[1]['name'] if cur[0] == 0 else acc +
        "," + cur[1]['name'],
        enumerate(artist_list),
        ""
    )
    artists_id = reduce(
        lambda acc, cur: cur[1]['id'] if cur[0] == 0 else acc +
        "," + cur[1]['id'],
        enumerate(artist_list),
        ""
    )

    track = pd.Series({
        "id": _id,
        "name": _name,
        "artistIds": artists_id,
        "artistNames": artists,
        "image": _image
    })

    if self.sel_tracks is None:
        self.sel_tracks = pd.DataFrame(track).T
    else:
        self.sel_tracks = self.sel_tracks.append(track, ignore_index=True)
