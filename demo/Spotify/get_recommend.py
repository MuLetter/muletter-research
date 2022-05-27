import pandas as pd
import numpy as np
import requests as req
from urllib.parse import urlencode
from functools import reduce


def get_recommend(self, og=None, get_bak=False):
    reco_url = "https://api.spotify.com/v1/recommendations"
    _reco_tracks = np.array([])
    for idx, _seed in self.seed.iterrows():
        query = _seed.to_dict()

        query['market'] = 'KR'
        query['limit'] = 100

        query = urlencode(query)
        headers = {
            "authorization": "Bearer {}".format(self.token)
        }
        try:
            res = req.get("{}?{}".format(reco_url, query), headers=headers)
            result = res.json()

            for track in result['tracks']:
                _id = track['id']
                _name = track['name']
                album = track['album']
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
                _reco_tracks = np.append(_reco_tracks,
                                         [_id, _name, artists_id, artists,
                                             _image, _seed['seed_tracks']]
                                         )
        except:
            return res

    _reco_tracks = _reco_tracks.reshape(-1, 6)
    reco_tracks = pd.DataFrame(_reco_tracks, columns=[
                               'trackId', 'trackName', 'artistIds', 'artistNames', 'image', 'seedId'])

    # 중복제거
    except_overlap_cols = [
        _ not in self.sel_tracks['trackId'].values for _ in reco_tracks['trackId']]
    reco_tracks = reco_tracks[except_overlap_cols]
    reco_tracks.drop_duplicates("trackId", inplace=True, ignore_index=True)

    if og is not None:
        reco_tracks = reco_tracks[[
            _ not in og['trackId'].values for _ in reco_tracks['trackId']]]

    self.reco_tracks = reco_tracks
