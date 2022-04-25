import numpy as np
import pandas as pd


def music_filtering(self):
    labels_ = self.kmeans.labels_

    cluster_res = pd.DataFrame(
        np.column_stack([self.features['trackId'], labels_]),
        columns=['trackId', 'label']
    )

    my_labels = np.unique(
        pd.merge(self.my_features, cluster_res, on='trackId')['label'].values)

    label_chk = np.isin(cluster_res['label'], my_labels)
    recos = cluster_res[label_chk].copy()

    my_tracks_chk = np.isin(recos['trackId'], self.my_tracks)
    recos = recos[~my_tracks_chk]

    return recos
