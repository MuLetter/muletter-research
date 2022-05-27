import numpy as np


def parse_reco_cluster(self):
    _labels = self.kmeans.labels_
    self.parsed_labels_ = np.unique(_labels[self.user_idx])

    reco_ids = self.merged['tracks'][np.isin(
        _labels, self.parsed_labels_)]['trackId'].values
    reco_ids = reco_ids[~np.isin(reco_ids, self.user['tracks']['trackId'])]

    _tracks = self.reco['tracks'][np.isin(
        self.reco['tracks']['trackId'], reco_ids)].copy().reset_index(drop=True)
    _features = self.reco['features'][np.isin(
        self.reco['features']['trackId'], reco_ids)].copy().reset_index(drop=True)

    self.reco_ = {
        "tracks": _tracks,
        "features": _features
    }
