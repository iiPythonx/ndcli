# Copyright (c) 2024 iiPython

# Modules
from typing import Any, List

from . import session
from ndcli.config import config

# Setup request handling
def make_request(method: str, endpoint: str, **kwargs) -> Any:
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

def get_artists(start: int, end: int, order: str, sort: str) -> List[dict]:
    return make_request("get", "api/artist", params = {"_start": start, "_end": end, "_order": order, "_sort": sort}).json()

def get_albums(start: int, end: int, order: str, sort: str) -> List[dict]:
    return make_request("get", "api/album", params = {"_start": start, "_end": end, "_order": order, "_sort": sort}).json()

def get_tracks(start: int, end: int, order: str, sort: str) -> List[dict]:
    return make_request("get", "api/song", params = {"_start": start, "_end": end, "_order": order, "_sort": sort}).json()
