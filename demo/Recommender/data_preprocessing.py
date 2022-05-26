def data_preprocessing(self):
    features = self.merged['features'].values
    norm_features = features[:, 1:]
    norm_features = (norm_features - norm_features.min(axis=0)) / \
        (norm_features.max(axis=0) - norm_features.min(axis=0))

    self.features = {
        "default": features,
        "norm": norm_features
    }
