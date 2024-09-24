# Copyright (c) 2024 iiPython

# Modules
from typing import Any

from requests import Session

from ndcli.config import config

# Initialization
session = Session()
def make_request(endpoint: str, method: str = "get", **kwargs) -> Any:
    return session.request(method.upper(), f"{config.get('server')}/{endpoint}", timeout = 5, **kwargs)
