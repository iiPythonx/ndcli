# Copyright (c) 2024 iiPython

# Modules
from typing import Callable

import click

from . import ndcli
from .show import show_item

from ndcli import console
from ndcli.api import navidrome
from ndcli.utils.paging import Paginator

# Commands
def handle_page(method: Callable, ascending: bool, sort: str, title_format: Callable) -> str:
    with console.status("[blue]Fetching data...", spinner = "arc"):
        results = [
            (a, title_format(a))
            for a in method(start = 0, end = 0, order = "ASC" if ascending else "DESC", sort = sort)
        ]

    return Paginator(results).render()

formatting = {
    "artists": (navidrome.get_artists, lambda a: a["name"]),
    "albums": (navidrome.get_albums, lambda a: f"{a['name']} [bright_black]({a['artist']})[/]"),
    "tracks": (navidrome.get_tracks, lambda a: f"{a['title']} [yellow]({a['album']})[/] [bright_black]({a['artist']})[/]")
}

@click.option("--asc", is_flag = True, show_default = True, default = False, help = "Show results in ascending order instead.")
@click.option("--sort", show_default = True, default = "title", type = str, help = "Field to sort results using.")
@click.argument("type", type = click.Choice(["artists", "albums", "tracks"], case_sensitive = False))
@ndcli.command("list")
def list_command(asc: bool, sort: str, type: str) -> None:
    """List artists, albums, & tracks."""
    sort = "name" if sort == "title" and type in ["artists", "albums"] else sort
    method, title_format = formatting[type]

    # Handle displaying selection
    data = handle_page(method, asc, sort, title_format)
    if type == "tracks":
        data = {
            "track": data["trackNumber"],
            "channelCount": data["channels"],
            "samplingRate": data["sampleRate"],
            "contentType": f"audio/{data['suffix']}",
            **data
        }

    show_item(data | {"type": type.rstrip("s") if type != "tracks" else "song"})
