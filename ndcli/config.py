# Copyright (c) 2024 iiPython

# Modules
import json
from typing import Any
from pathlib import Path

# Handle configuration
class Config():
    def __init__(self) -> None:
        self.config_file = Path.home() / ".config/ndcli/token.json"
        self.config_file.parent.mkdir(parents = True, exist_ok = True)

        # Load from existing file
        self.config = {}
        if self.config_file.is_file():
            self.config = json.loads(self.config_file.read_text())

    def get(self, key: str) -> Any:
        return self.config.get(key)

    def set(self, key: str, value: Any) -> None:
        self.config[key] = value
        self.config_file.write_text(json.dumps(self.config, indent = 4))

config = Config()
