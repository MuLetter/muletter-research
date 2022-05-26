import numpy as np
import pandas as pd
from functools import reduce
from .common import FEATURE_COLS


def set_seed(self):
    seed = pd.DataFrame(columns=['seed_tracks', 'seed_artists', 'seed_genres'])
    tracks = self.sel_tracks.copy()
    genres = self.genres.copy()
    features = self.features.copy()

    for idx, track in tracks.iterrows():
        # Track Id
        seed_tracks = track['trackId']

        # 아티스트 조합
        seed_artists = track['artistIds']

        seed_genres = np.array([])
        for artist in seed_artists.split(","):
            _genres = np.array(
                genres[genres['artistIds'] ==
                       artist]['genres'].values[0].split(",")
            )
            # 장르 중복 회피
            _genres = _genres[~np.isin(_genres, seed_genres)]
            seed_genres = np.append(seed_genres, _genres)
        # 장르 조합
        seed_genres = reduce(lambda acc, cur: acc +
                             "," + cur, seed_genres, "")[1:]

        # Seed In
        seed = seed.append({
            "seed_tracks": seed_tracks,
            "seed_artists": seed_artists,
            "seed_genres": seed_genres
        }, ignore_index=True)

    # Max 5 Check
    for idx, _seed in seed.iterrows():
        seed_dict = _seed.to_dict()
        while True:
            seed_counts = list()
            for value in seed_dict.values():
                split_value = value.split(",")
                seed_counts.append(len(split_value))

            if sum(seed_counts) > 5:
                max_seed_feature_idx = np.array(seed_counts).argmax()
                keys = list(seed_dict.keys())
                target = seed_dict[keys[max_seed_feature_idx]].split(",")

                remove_idx = np.random.choice(len(target))
                remove_target = np.delete(target, remove_idx)

                seed_dict[keys[max_seed_feature_idx]] = reduce(
                    lambda acc, cur: acc + "," + cur,
                    remove_target,
                    ""
                )[1:]
            else:
                seed.iloc[idx] = seed_dict
                break

    target_cols = seed.columns.tolist() + FEATURE_COLS
    seed = pd.merge(
        left=seed, right=features, how='inner', left_on='seed_tracks', right_on='trackId')[target_cols]

    change_feature_cols = dict()
    for FEATURE in FEATURE_COLS:
        change_feature_cols[FEATURE] = "target_" + FEATURE

    self.seed = seed.rename(change_feature_cols, axis=1)
