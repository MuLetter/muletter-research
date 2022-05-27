# from ..Recommender import Recommender

import pandas as pd
import numpy as np
from sklearn.metrics import euclidean_distances as euc


def max_adjust_rate(self, _count):
    user_track_ids = self.user['tracks']['trackId']
    user_norm_features = dict()

    for user_track_id in user_track_ids:
        chk = np.any(np.isin(self.features['default'], user_track_id), axis=1)
        user_norm_features[user_track_id] = self.features['norm'][chk]

    max_idx = _count.idxmax()
    user_features = user_norm_features[max_idx]

    reco_features = self.features['norm'][np.isin(
        self.merged['tracks']['trackId'],
        self.reco_['tracks']['trackId'])]
    reco_features = reco_features[np.isin(
        self.reco_['tracks']['seedId'], max_idx)]

    _arg_max_dis = euc(user_features, reco_features).argmax()
    arg_max_ids = self.reco_['tracks'][np.isin(
        self.reco_['tracks']['seedId'], max_idx)].iloc[_arg_max_dis].name

    for key in self.reco_.keys():
        self.reco_[key].drop(arg_max_ids, inplace=True)
        self.reco_[key].reset_index(drop=True, inplace=True)


def min_adjust_rate(self):
    user = self.user.copy()
    reco = dict()
    for key in self.reco.keys():
        reco[key] = self.reco[key][
            ~np.isin(self.reco[key]['trackId'], self.reco_[key]['trackId'])
        ].copy().reset_index(drop=True)

    _recommender = self.generate()
    _recommender.static_setting(user, reco)
    _recommender.merge()
    _recommender.data_preprocessing()
    _recommender.run()

    for key in self.reco_.keys():
        self.reco_[key] = pd.concat([
            self.reco_[key],
            _recommender.reco_[key]
        ]).reset_index(drop=True)


def adjust_rate(self):
    while True:
        _count = self.reco_['tracks']['seedId'].value_counts()
        if _count.sum() > 100:
            max_adjust_rate(self, _count)
        elif _count.sum() < 50:
            min_adjust_rate(self)
        else:
            self.count_ = _count
            break
