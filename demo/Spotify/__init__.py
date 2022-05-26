from .get_token import get_token
from .search import search
from .get_features import get_features
from .get_genres import get_genres


class Spotify:
    def __init__(self, sel_tracks=None):
        self.get_token()
        self.sel_tracks = sel_tracks


Spotify.get_token = get_token
Spotify.search = search
Spotify.get_features = get_features
Spotify.get_genres = get_genres
