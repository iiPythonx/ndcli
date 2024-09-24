# Copyright (c) 2024 iiPython

# Modules
import os
from typing import Any

from requests import Session

from ndcli.config import config

# Initialization
os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"

session = Session()
def make_request(endpoint: str, method: str = "get", **kwargs) -> Any:
    return session.request(
        method.upper(),
        f"{config.get('server')}/{endpoint}",
        timeout = 5,
        headers = {"X-Nd-Authorization": f"Bearer: {config.get('auth')['nt']}"},
        **kwargs
    )
