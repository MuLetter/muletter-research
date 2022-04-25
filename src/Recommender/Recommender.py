import pandas as pd

from ..utils import DB
from .. import Spotify


class Recommender:
    def __init__(self, mail_box_id):
        self.db = DB()
        self.mail_box_id = mail_box_id

    def init_setting(self):
        mail_box = self.db.get_mailbox(self.mail_box_id)

        cols = ['trackId', 'trackName', 'artistIds', 'artistNames', 'image']

        _sel_tracks = mail_box['tracks']
        sel_tracks = pd.DataFrame(_sel_tracks)[cols]

        sp = Spotify(sel_tracks)
        sp.get_genres()
        sp.get_features()
        sp.get_recommend()

        reco_sp = Spotify(sp.reco_tracks)
        reco_sp.get_features()

        self.my_tracks = sp.sel_tracks
        self.my_features = sp.features

        self.reco_tracks = reco_sp.sel_tracks
        self.reco_features = reco_sp.features

        self.features = pd.concat([self.my_features, self.reco_features])

    def data_preprocessing(self):
        features = pd.concat([self.my_features, self.reco_features])

        norm_features = features.values[:, 1:]
        norm_features = (norm_features - norm_features.min(axis=0)) / \
                        (norm_features.max(axis=0) - norm_features.min(axis=0))

        self.norm_features = norm_features
