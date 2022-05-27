import pandas as pd

from .merge import merge
from .data_preprocessing import data_preprocessing
from .run import run
from .draw_dataset import draw_dataset
from .draw_cluster import draw_cluster
from .parse_reco_cluster import parse_reco_cluster


from ..Spotify import Spotify
from ..lib.DB import DB


class Recommender:
    def __init__(self, mailbox_id):
        self.db = DB()
        self.mailbox = self.db.get_mailbox(mailbox_id)
        tracks = self.mailbox['tracks']

        user_tracks = pd.DataFrame(tracks)
        sp = Spotify(user_tracks)
        sp.auto_reco_process()

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


Recommender.merge = merge
Recommender.data_preprocessing = data_preprocessing
Recommender.draw_dataset = draw_dataset
Recommender.draw_cluster = draw_cluster
Recommender.run = run
Recommender.parse_reco_cluster = parse_reco_cluster
