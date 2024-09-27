# Copyright (c) 2024 iiPython

# Modules
import os
import urllib3
from typing import Any, List, Sequence

from requests import PreparedRequest, Session, Request

from .typing import Artist, Album, Track, TypedObject

from ndcli import __version__
from ndcli.config import config

# Initialization
os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"
urllib3.disable_warnings()

# Setup API handling
class Navidrome():
    def __init__(self) -> None:
        self.auth = config.get("auth") or {}
        self.server = config.get("server")
        self.session = Session()

        # Navidrome parameters
        self.__parameter_map = {
            "start": "_start", "end": "_end", "order": "_order", "sort": "_sort"
        }

    # Handle actual request making
    def build_subsonic(self, method: str, endpoint: str, **kwargs) -> PreparedRequest:
        kwargs["params"] = kwargs.get("params", {}) | {
            "c": "ndcli",
            "f": "json",
            "v": __version__,
            "u": self.auth["username"],
            "s": self.auth["subsonicSalt"],
            "t": self.auth["subsonicToken"]
        }
        return Request(
            method.upper(),
            f"{self.server}/rest/{endpoint}",
            **kwargs
        ).prepare()

    def request_subsonic(self, *args, **kwargs) -> Any:
        return self.session.send(self.build_subsonic(*args, **kwargs), timeout = 5, verify = False).json()["subsonic-response"]

    def request_navidrome(self, method: str, endpoint: str, **kwargs) -> Any:
        kwargs["params"] = {
            self.__parameter_map.get(k, k): v
            for k, v in kwargs.get("params", {}).items()
        }
        return self.session.request(
            method.upper(),
            f"{self.server}/{endpoint}",
            timeout = 5,
            verify = False,
            headers = {"X-Nd-Authorization": f"Bearer: {self.auth.get('token')}"},
            **kwargs
        )

    # Handle subsonic endpoints
    def search(
        self,
        query: str,
        album_count: int,
        artist_count: int,
        song_count: int,
        album_offset: int = 0,
        artist_offset: int = 0,
        song_offset: int = 0,
    ) -> Sequence[TypedObject]:
        response = self.request_subsonic("get", "search3.view", params = {
            "query": query,
            "albumCount": album_count,
            "albumOffset": album_offset,
            "artistCount": artist_count,
            "artistOffset": artist_offset,
            "songCount": song_count,
            "songOffset": song_offset
        })["searchResult3"]
        return [self.get_artist(artist["id"]) for artist in response.get("artist", [])] + \
                [self.get_album(album["id"]) for album in response.get("album", [])] + \
                [Track(track) for track in response.get("song", [])]

    def get_top_songs(self, artist: str) -> List[Track]:
        return [
            Track(track) for track in
            self.request_subsonic("get", "getTopSongs.view", params = {"artist": artist})["topSongs"]["song"]
        ]

    # Handle navidrome endpoints
    def ping(self) -> int:
        return self.request_navidrome("get", "ping").status_code

    def login(self, username: str, password: str) -> dict:
        return self.request_navidrome("post", "auth/login", json = {"username": username, "password": password}).json()

    def get_artists(self, **kwargs) -> List[Artist]:
        return [
            Artist(artist) for artist in
            self.request_navidrome("get", "api/artist", params = kwargs).json()
        ]

    def get_albums(self, **kwargs) -> List[Album]:
        return [
            Album(album) for album in
            self.request_navidrome("get", "api/album", params = kwargs).json()
        ]

    def get_tracks(self, **kwargs) -> List[Track]:
        return [
            Track(track) for track in
            self.request_navidrome("get", "api/song", params = kwargs).json()
        ]

    def get_artist(self, artist_id: str) -> Artist:
        return Artist(self.request_navidrome("get", f"api/artist/{artist_id}").json())

    def get_album(self, album_id: str) -> Album:
        return Album(self.request_navidrome("get", f"api/album/{album_id}").json())

navidrome = Navidrome()
