import pandas as pd
import requests as req
from urllib.parse import urlencode
import math as mt


def get_features(self):
    features_uri = "https://api.spotify.com/v1/audio-features"
    headers = {
        "authorization": "Bearer {}".format(self.token)
    }
    cnt = mt.floor((len(self.sel_tracks) - 1) / 100) + 1

    features = pd.DataFrame()
    target_cols = ['id', 'danceability', 'energy', 'key', 'loudness', 'speechiness',
                   'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

    for _cnt in range(0, cnt):
        ids = ""
        for track_id in self.sel_tracks[_cnt * 100: (_cnt + 1) * 100]['trackId']:
            split_data = track_id.split(",")

            for _ in split_data:
                ids += "{},".format(_)

        ids = ids[:-1]

        query = urlencode({
            "ids": ids
        })

        res = req.get("{}?{}".format(features_uri, query), headers=headers)
        result = res.json()
        features = pd.concat([features, pd.DataFrame(
            list(filter(lambda x: x is not None, result['audio_features'])))[target_cols]], ignore_index=True)

    self.features = features.rename({"id": "trackId"}, axis=1)
