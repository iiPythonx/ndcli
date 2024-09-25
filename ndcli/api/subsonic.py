# Copyright (c) 2024 iiPython

# Modules
from typing import Any, List

from . import session
from ndcli import __version__
from ndcli.config import config

# Setup request handling
def make_request(method: str, endpoint: str, **kwargs) -> Any:
    kwargs["params"] = kwargs.get("params", {}) | {
        "c": "ndcli",
        "f": "json",
        "v": __version__,
        "u": config.get("auth")["un"],
        "s": config.get("auth")["ss"],
        "t": config.get("auth")["st"]
    }
    return session.request(
        method.upper(),
        f"{config.get('server')}/rest/{endpoint}",
        timeout = 5,
        **kwargs
    ).json()["subsonic-response"]

# Subsonic handling
def search(
    query: str,
    album_count: int,
    artist_count: int,
    song_count: int,
    album_offset: int = 0,
    artist_offset: int = 0,
    song_offset: int = 0,
) -> List[dict]:
    return make_request("get", "search3.view", params = {
        "query": query,
        "albumCount": album_count,
        "albumOffset": album_offset,
        "artistCount": artist_count,
        "artistOffset": artist_offset,
        "songCount": song_count,
        "songOffset": song_offset
    })["searchResult3"]

def get_top_songs(artist: str) -> List[dict]:
    return make_request("get", "getTopSongs.view", params = {"artist": artist})["topSongs"]["song"]
