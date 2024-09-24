# Copyright (c) 2024 iiPython

# Modules
import os
from requests import Session

# Initialization
os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"
session = Session()
