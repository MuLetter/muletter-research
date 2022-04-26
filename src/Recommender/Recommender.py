import pandas as pd
import numpy as np

from ..utils import DB
from .. import Spotify
from ..utils.KMeans import KMeans
from .init_setting import init_setting
from .data_preprocessing import data_preprocessing
from .music_filtering import music_filtering
from sklearn.metrics.pairwise import euclidean_distances as euc


class Recommender:
    def __init__(self, mail_box_id):
        self.db = DB()
        self.mail_box_id = mail_box_id

    def reco_musics(self):
        MAX_COUNT = 100
        MIN_COUNT = 50

        reco_mem = np.array([])
        _reco_tracks = self.reco_tracks.copy()
        _reco_features = self.reco_features.copy()

        while True:
            print("Start!")
            self.kmeans = KMeans(self.norm_features)
            self.kmeans.fit()

            recos = music_filtering(self)

            if (len(recos) + reco_mem.size) > MAX_COUNT:
                while True:
                    clusters_ = self.kmeans.clusters_
                    cnt_df = recos.groupby("label").count()

                    max_label = cnt_df['trackId'].idxmax()
                    chk_idxes = recos[recos['label'] == max_label].index

                    chk_cluster = np.expand_dims(clusters_[max_label], axis=0)
                    chk_features = self.norm_features[chk_idxes]

                    max_idx = euc(chk_cluster, chk_features).argmax()
                    recos.drop(chk_idxes[max_idx], inplace=True)

                    if len(recos) <= MAX_COUNT:
                        reco_mem = np.append(reco_mem, recos['trackId'].values)
                        break
                break
            elif (len(recos) + reco_mem.size) < MIN_COUNT:
                reco_mem = np.append(reco_mem, recos['trackId'].values)

                self.reco_tracks = self.reco_tracks[~np.isin(
                    self.reco_tracks['trackId'], reco_mem)]
                self.reco_features = self.reco_features[~np.isin(
                    self.reco_features['trackId'], reco_mem)]

                self.data_preprocessing()
            else:
                reco_mem = np.append(reco_mem, recos['trackId'].values)
                break

        self.reco_musics_df = _reco_tracks[np.isin(
            _reco_tracks['trackId'], reco_mem)].sample(frac=1).copy()

        print("[Recommender] Reco Musics Setting Okay :)")


Recommender.init_setting = init_setting
Recommender.data_preprocessing = data_preprocessing
Recommender.music_filtering = music_filtering
