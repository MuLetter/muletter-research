import pandas as pd

from .merge import merge
from .data_preprocessing import data_preprocessing
from .run import run
from .draw_dataset import draw_dataset
from .draw_cluster import draw_cluster
from .parse_reco_cluster import parse_reco_cluster
from .adjust_rate import adjust_rate
from .draw_rate import draw_rate
from .draw_filtering import draw_filtering


from ..Spotify import Spotify
from ..lib.DB import DB


class Recommender:
    def __init__(self, mailbox_id=None):
        self.db = DB()
        self.mailbox_id = mailbox_id
        if mailbox_id is not None:
            self.mailbox = self.db.get_mailbox(mailbox_id)

    def generate(self):
        return Recommender()

    def init_setting(self):
        tracks = self.mailbox['tracks']

        user_tracks = pd.DataFrame(tracks)
        sp = Spotify(user_tracks)
        sp.auto_reco_process()
        self.db.save_seedzone(sp.features)

        reco_tracks = sp.reco_tracks
        reco_sp = Spotify(reco_tracks)
        reco_sp.get_features()

        self.user = {
            "tracks": user_tracks,
            "features": sp.features,
        }
        self.reco = {
            "tracks": reco_tracks,
            "features": reco_sp.features
        }

    def static_setting(self, user, reco):
        self.user = user
        self.reco = reco


Recommender.merge = merge
Recommender.data_preprocessing = data_preprocessing
Recommender.draw_dataset = draw_dataset
Recommender.draw_cluster = draw_cluster
Recommender.run = run
Recommender.parse_reco_cluster = parse_reco_cluster
Recommender.adjust_rate = adjust_rate
Recommender.draw_rate = draw_rate
Recommender.draw_filtering = draw_filtering
