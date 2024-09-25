# Copyright (c) 2024 iiPython

# Modules
from typing import Any, List

from . import session
from ndcli.config import config

# Setup request handling
parameter_mapping = {
    "start": "_start", "end": "_end", "order": "_order", "sort": "_sort"
}

def make_request(method: str, endpoint: str, **kwargs) -> Any:
    kwargs["params"] = {
        parameter_mapping.get(k, k): v
        for k, v in kwargs.get("params", {}).items()
    }
    return session.request(
        method.upper(),
        f"{config.get('server')}/{endpoint}",
        timeout = 5,
        headers = {"X-Nd-Authorization": f"Bearer: {config.get('auth')['nt']}"},
        **kwargs
    )

# Navidrome handling
def ping() -> int:
    return make_request("get", "ping").status_code

def login(username: str, password: str) -> dict:
    return make_request("post", "auth/login", json = {"username": username, "password": password}).json()

# Searching (non-specific)
def get_artists(**kwargs) -> List[dict]:
    return make_request("get", "api/artist", params = kwargs).json()

def get_albums(**kwargs) -> List[dict]:
    return make_request("get", "api/album", params = kwargs).json()

def get_tracks(**kwargs) -> List[dict]:
    return make_request("get", "api/song", params = kwargs).json()

# Fetch by ID (specific)
def get_artist(artist_id: str) -> dict:
    return make_request("get", f"api/artist/{artist_id}").json()

def get_album(album_id: str) -> dict:
    return make_request("get", f"api/album/{album_id}").json()
