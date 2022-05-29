import pandas as pd
import math as mt

from ..lib import DB, KMeans
from ..common import FEATURE_COLS


class SeedZoneObserver:
    def __init__(self):
        self.db = DB()

    @staticmethod
    def observe():
        db = DB()

        seed_zone_count = db.seed_zone.estimated_document_count()
        check_K = round(mt.sqrt(seed_zone_count / 2))

        K = db.cluster_zone.find({}).sort("createdAt", -1)[0]["K"]

        return check_K, K

    def run(self, drawing=False):
        # Data Ready
        seeds = self.db.seed_zone.find({}, {"_id": 0})

        # Data Preprocessing
        features = pd.DataFrame([_ for _ in seeds])[
            ['trackId'] + FEATURE_COLS].to_numpy()
        norm_features = (features[:, 1:] - features[:, 1:].min(axis=0)) / \
            (features[:, 1:].max(axis=0) - features[:, 1:].min(axis=0))

        # KMeans Run
        kmeans = KMeans(norm_features)
        kmeans.init_setting()
        kmeans.fit()
        kmeans.sorting()

        self.features = features
        self.kmeans = kmeans

        self.db.save_clusterzone(self)
