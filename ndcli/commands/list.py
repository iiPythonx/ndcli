# Copyright (c) 2024 iiPython

# Modules
from typing import Callable

import click

from . import ndcli

from ndcli import console
from ndcli.api import navidrome
from ndcli.utils.paging import Paginator

# Group
@ndcli.group("list")
def list_group() -> None:
    """List artists, albums, & tracks."""
    return

# Commands
def handle_page(method: Callable, ascending: bool, sort: str, title_format: Callable) -> str:
    with console.status("[blue]Fetching data...", spinner = "arc"):
        results = [
            (a["id"], title_format(a))
            for a in method(0, 0, "ASC" if ascending else "DESC", sort)
        ]

    return Paginator(results).render()

for name, method, title_format in [
    ("artists", navidrome.get_artists, lambda a: a["name"]),
    ("albums", navidrome.get_albums, lambda a: f"{a['name']} [bright_black]({a['artist']})[/]"),
    ("tracks", navidrome.get_tracks, lambda a: f"{a['title']} [yellow]({a['album']})[/] [bright_black]({a['artist']})[/]")
]:

    @click.option("--asc", is_flag = True, show_default = True, default = False, help = "Show results in ascending order instead.")
    @click.option("--sort", show_default = True, default = "title", type = str, help = "Field to sort results using.")
    def command(asc: bool, sort: str):
        print(handle_page(method, asc, sort, title_format))

    list_group.add_command(click.command(name, help = f"List all {name} on the Navidrome instance.")(command))
