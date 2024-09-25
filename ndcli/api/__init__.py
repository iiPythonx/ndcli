# Copyright (c) 2024 iiPython

# Modules
import os
import urllib3

from requests import Session

# Initialization
os.environ["REQUESTS_CA_BUNDLE"] = "/etc/ssl/certs/ca-certificates.crt"
urllib3.disable_warnings()

session = Session()
