import pandas as pd
from ..lib import DB, KMeans


class SeedZoneObserver:
    @staticmethod
    def observe():
        db = DB()
        return db.seed_zone.estimated_document_count()

    def run(self, drawing=False):
        db = DB()

        # Data Ready
        seeds = db.seed_zone.find({}, {"_id": 0})

        # Data Preprocessing
        features = pd.DataFrame([_ for _ in seeds]).to_numpy()
        norm_features = (features[:, 1:] - features[:, 1:].min(axis=0)) / \
            (features[:, 1:].max(axis=0) - features[:, 1:].min(axis=0))

        # KMeans Run
        kmeans = KMeans(norm_features)
        kmeans.init_setting()
        kmeans.fit()
        kmeans.sorting()

        self.features = features
        self.kmeans = kmeans
