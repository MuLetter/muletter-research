from .get_token import get_token
from .search import search
from .get_features import get_features
from .get_genres import get_genres
from .get_recommend import get_recommend
from .set_seed import set_seed
from .get_track import get_track


class Spotify:
    def __init__(self, sel_tracks=None):
        self.get_token()
        self.sel_tracks = sel_tracks

    def auto_reco_process(self):
        self.get_genres()
        self.get_features()
        self.set_seed()
        self.get_recommend()


Spotify.get_token = get_token
Spotify.search = search
Spotify.get_features = get_features
Spotify.get_genres = get_genres
Spotify.get_recommend = get_recommend
Spotify.set_seed = set_seed
Spotify.get_track = get_track
