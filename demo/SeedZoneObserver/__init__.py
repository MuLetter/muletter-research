import pandas as pd
import math as mt

from ..lib import DB, KMeans
from ..common import FEATURE_COLS


class SeedZoneObserver:
    def __init__(self):
        self.db = DB()

    def init_setting(self):
        # Data Ready
        seeds = self.db.seed_zone.find({}, {"_id": 0})

        # Data Preprocessing
        self.features_df = pd.DataFrame([_ for _ in seeds])[
            ['trackId'] + FEATURE_COLS]
        self.features = self.features_df.to_numpy()
        self.norm_features = (self.features[:, 1:] - self.features[:, 1:].min(axis=0)) / \
            (self.features[:, 1:].max(axis=0) -
             self.features[:, 1:].min(axis=0))

    @staticmethod
    def observe():
        db = DB()

        seed_zone_count = db.seed_zone.estimated_document_count()
        check_K = round(mt.sqrt(seed_zone_count / 2))

        K = db.cluster_zone.find({}).sort("createdAt", -1)[0]["K"]

        return check_K, K

    def run(self, drawing=False):

        # KMeans Run
        kmeans = KMeans(self.norm_features)
        kmeans.init_setting()
        kmeans.fit()

        self.kmeans = kmeans

    def sorting(self):
        self.kmeans.sorting()

    def save(self):
        self.cluster_zone = self.db.save_clusterzone(self)
