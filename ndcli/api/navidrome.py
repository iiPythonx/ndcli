# Copyright (c) 2024 iiPython

# Modules
from typing import List

from . import make_request

# Navidrome handling
def ping() -> int:
    return make_request("ping").status_code

def login(username: str, password: str) -> dict:
    return make_request("auth/login", "post", json = {"username": username, "password": password}).json()

def get_artists(start: int, end: int, order: str, sort: str) -> List[dict]:
    return make_request("api/artist", params = {"_start": start, "_end": end, "_order": order, "_sort": sort}).json()

def get_albums(start: int, end: int, order: str, sort: str) -> List[dict]:
    return make_request("api/album", params = {"_start": start, "_end": end, "_order": order, "_sort": sort}).json()

def get_tracks(start: int, end: int, order: str, sort: str) -> List[dict]:
    return make_request("api/song", params = {"_start": start, "_end": end, "_order": order, "_sort": sort}).json()
