# Copyright (c) 2024 iiPython

from .commands import ndcli  # noqa: F401

# Dynamically import our commands
import importlib
from pathlib import Path
[
    importlib.import_module(f"ndcli.commands.{file.with_suffix('').name}")
    for file in (Path(__file__).parent / "commands").iterdir()
]
