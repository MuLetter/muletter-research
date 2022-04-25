import pandas as pd


def data_preprocessing(self):
    # 1. 데이터 병합
    self.features = pd.concat([self.my_features, self.reco_features])

    # 2. 데이터 정규화
    norm_features = self.features.values[:, 1:]
    norm_features = (norm_features - norm_features.min(axis=0)) / \
        (norm_features.max(axis=0) - norm_features.min(axis=0))

    self.norm_features = norm_features
