import pandas as pd
import numpy as np


def merge(self):
    merge = dict()

    for key in self.user.keys():
        user = self.user[key].copy()
        reco = self.reco[key].copy()

        merge[key] = pd.concat([user, reco], ignore_index=True)

    self.user_idx = np.isin(
        merge['tracks']['trackId'], self.user['tracks']['trackId'])
    self.merged = merge
