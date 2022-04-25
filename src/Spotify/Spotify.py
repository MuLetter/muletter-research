from .get_token import get_token
from .search import search
from .get_genres import get_genres
from .get_features import get_features
from .get_recommend import get_recommend


class Spotify:
    def __init__(self, sel_tracks=None):
        self.get_token()
        self.sel_tracks = sel_tracks


Spotify.get_token = get_token
Spotify.search = search
Spotify.get_genres = get_genres
Spotify.get_features = get_features
Spotify.get_recommend = get_recommend
