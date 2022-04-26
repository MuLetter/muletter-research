from pyexpat import features
import pandas as pd


def data_preprocessing(self):
    # 1. 데이터 병합

    self.features = pd.concat(
        [self.my_features, self.reco_features], ignore_index=True)

    # 2. 데이터 정규화
    norm_features = self.features.values[:, 1:]
    norm_features = (norm_features - norm_features.min(axis=0)) / \
        (norm_features.max(axis=0) - norm_features.min(axis=0))

    self.norm_features = norm_features

    if ~self.is_run:
        self.features_bak = self.features.copy()
        self.norm_features_bak = self.norm_features.copy()
