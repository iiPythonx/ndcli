# Copyright (c) 2024 iiPython

# Modules
import click
from rich.console import Console
from requests.exceptions import ConnectionError, Timeout

from .api import navidrome
from .config import config

# Initialization
console = Console()
def erase_last_line(text: str | None = None, lines: int = 1) -> None:
    print(f"\033[{lines}F\033[2K", end = "")  # This is fun.
    if text is not None:
        console.print(text)

# Handle group
@click.group()
def ndcli() -> None:
    """A CLI for interacting with the Navidrome/Subsonic API."""
    return

# Handle commands
@ndcli.command()
def login() -> None:
    """Authenticate with Navidrome."""
    server_url = console.input("[blue]Navidrome URL: ").rstrip("/")
    if "://" not in server_url:
        if ":" not in server_url:
            server_url += ":4533"

        server_url = f"http://{server_url}"

    config.set("server", server_url)
    erase_last_line(f"[blue]Navidrome URL: {server_url}")
    
    # Check status of input
    with console.status("[blue]Checking URL...", spinner = "arc"):
        try:
            response_status = navidrome.ping()

        except (ConnectionError, Timeout):
            response_status = 500

    erase_last_line(f"[{'red' if response_status != 200 else 'green'}]Navidrome URL: {server_url}")
    if response_status != 200:
        return console.print("[red]Connection to specified server failed, check your URL.")

    # Attempt to login
    username, password = console.input("[blue]Navidrome username: "), console.input("[blue]Navidrome password: ", password = True)
    with console.status("[blue]Logging in...", spinner = "arc"):
        result = navidrome.login(username, password)

    if "error" in result:
        return erase_last_line(f"[red]{result['error']}.", 2)

    config.set("auth", {
        "ss": result["subsonicSalt"],
        "st": result["subsonicToken"],
        "nt": result["token"]
    })
    return erase_last_line(f"[green]Logged in as {result['username']}.", 2)
