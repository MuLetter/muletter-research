import pandas as pd
import numpy as np
import requests as req
from urllib.parse import urlencode
from functools import reduce


def get_recommend(self, og=None, get_bak=False):
    _sel_tracks = pd.DataFrame()

    for idx, row in self.sel_tracks.iterrows():
        artist_ids = row['artistIds'].split(",")
        artist_names = row['artistNames'].split(",")
        if len(artist_ids) > 1:
            for _idx, artist_id in enumerate(artist_ids):
                _row = row.copy()
                artist_name = artist_names[_idx]
                _row['artistIds'] = artist_id
                _row['artistNames'] = artist_name
                _sel_tracks = _sel_tracks.append(_row,
                                                 ignore_index=True)
        else:
            _sel_tracks = _sel_tracks.append(row,
                                             ignore_index=True)

    try:
        seed_info = pd.merge(
            left=_sel_tracks, right=self.features, how='inner', on='trackId')
        seed_info = pd.merge(left=seed_info, right=self.genres,
                             how='inner', on='artistIds')

    except:
        return self.sel_tracks, self.features

    seed_info.rename({
        "trackId": "seed_tracks",
        "artistIds": "seed_artists",
        "genres": "seed_genres",
    }, axis=1, inplace=True)
    feature_cols = ['seed_tracks', 'seed_artists', 'seed_genres',
                    'acousticness', 'danceability', 'energy',
                    'instrumentalness', 'key', 'liveness', 'loudness',
                    'speechiness', 'tempo', 'valence']
    seed_info = seed_info[feature_cols]

    reco_url = "https://api.spotify.com/v1/recommendations"
    _reco_tracks = np.array([])
    for idx in range(len(seed_info)):
        query = seed_info.iloc[idx].to_dict()
        seed_id = query['seed_tracks']
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
                                             _image, seed_id]
                                         )
        except:
            return res

    _reco_tracks = _reco_tracks.reshape(-1, 6)
    reco_tracks = pd.DataFrame(_reco_tracks, columns=[
                               'trackId', 'trackName', 'artistIds', 'artistName', 'image', 'seedId'])

    # 중복제거
    except_overlap_cols = [
        _ not in self.sel_tracks['trackId'].values for _ in reco_tracks['trackId']]
    reco_tracks = reco_tracks[except_overlap_cols]
    reco_tracks.drop_duplicates("trackId", inplace=True)

    if og is not None:
        reco_tracks = reco_tracks[[
            _ not in og['trackId'].values for _ in reco_tracks['trackId']]]

    self.reco_tracks = reco_tracks
