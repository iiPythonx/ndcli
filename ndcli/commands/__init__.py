# Copyright (c) 2024 iiPython

# Modules
import click
from .. import console

# Initialization
def erase_last_line(text: str | None = None, lines: int = 1) -> None:
    print(f"\033[{lines}F\033[2K", end = "")  # This is fun.
    if text is not None:
        console.print(text)

# Handle group
@click.group(epilog = "Copyright (c) 2024 iiPython")
def ndcli() -> None:
    """A CLI for interacting with the Navidrome/Subsonic API.
    
    \b
    Source code: https://github.com/iiPythonx/ndcli
    """
    return
