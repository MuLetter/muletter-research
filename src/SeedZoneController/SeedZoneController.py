import pandas as pd
import numpy as np
import datetime as dt

from ..utils.KMeans import KMeans
from ..CoordGenerator import CoordGenerator

from pymongo import MongoClient as mc


class SeedZoneController:
    def __init__(self):
        mongo_uri = "mongodb://localhost:27017"
        self.conn = mc(mongo_uri).TestMuLetter
        self.seed_zone = self.conn.SeedZone
        self.mail_box = self.conn.MailBox
        self.cluster_zone = self.conn.ClusterZone
        self.coord_gen = CoordGenerator()

    def make_new_cluster(self):
        _seed_features = self.seed_zone.find({}, {
            "_id": 0,
            "label": 0
        })
        self.seed_features = pd.DataFrame([_ for _ in _seed_features])
        _seed_features = self.seed_features.iloc[:, 1:].values.copy()
        self.norm_features = (_seed_features - _seed_features.min(axis=0)) /\
            (_seed_features.max(axis=0) - _seed_features.min(axis=0))

        self.kmeans = KMeans(self.norm_features)
        self.kmeans.fit()
        self.kmeans.sorting()

    def save(self):
        version = self.cluster_zone.estimated_document_count() + 1
        features = self.kmeans.clusters_.tolist()
        ecv = round(self.kmeans.ecv * 100)
        K = self.kmeans.K
        createdAt = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

        _seed_features = self.seed_features.iloc[:, 1:].values.copy()

        min_norm_info = _seed_features.min(axis=0)
        max_norm_info = _seed_features.max(axis=0)
        _norm_info = np.column_stack((min_norm_info, max_norm_info)).tolist()

        norm_info = dict()
        for idx, col in enumerate(self.seed_features.columns[1:].values):
            norm_info[col] = _norm_info[idx]

        self.cluster_zone.insert_one({
            "version": version,
            "norm": norm_info,
            "features": features,
            "ecv": ecv,
            "K": K,
            "createdAt": createdAt
        })

        cluster_info = pd.DataFrame(
            np.column_stack(
                (self.seed_features['trackId'].values, self.kmeans.labels_)),
            columns=['trackId', 'label']
        )

        for idx, row in cluster_info.iterrows():
            self.seed_zone.update_one({
                "trackId": row['trackId']
            }, {
                "$set": {
                    "label": row['label']
                }
            })

        self.coord_gen.all_remake_coords()
        print("Save Okay :)")
