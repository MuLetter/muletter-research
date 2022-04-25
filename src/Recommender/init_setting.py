from .. import Spotify
import pandas as pd


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
