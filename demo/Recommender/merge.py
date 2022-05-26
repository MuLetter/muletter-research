import pandas as pd


def merge(self):
    merge = dict()

    for key in self.user.keys():
        user = self.user[key].copy()
        reco = self.reco[key].copy()

        merge[key] = pd.concat([user, reco], ignore_index=True)

    self.merged = merge
