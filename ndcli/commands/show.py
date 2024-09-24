# Copyright (c) 2024 iiPython

# Modules
import click

from . import ndcli

from ndcli import console
from ndcli.api import subsonic
from ndcli.utils.paging import Paginator

# Commands
@ndcli.command("show", default_command = True)
@click.argument("query", nargs = -1)
def show_command(query: str) -> None:
    """Search and show any Navidrome item."""

    # Normalize our query
    actual_query = " ".join(query).strip().lower()
    with console.status("[blue]Searching...", spinner = "arc"):
        response = subsonic.search(actual_query, 4, 4, 4)

    # Begin matching
    results = []
    for item_type, items in response.items():
        for item in items:
            results.append(item | {"type": item_type})

    direct_matches = []
    for item in results:
        if item["title" if item["type"] == "song" else "name"].lower() == actual_query:
            direct_matches.append(item)

    if len(direct_matches) == 1:
        return print("direct match", direct_matches[0])

    # Handle selection
    page_items = []
    for item in results:
        text = f"{item['title' if item['type'] == 'song' else 'name']} [bright_black]({item['type'].capitalize()})"
        if item["type"] in ["song", "album"]:
            text = text[:-1] + f", [yellow]{item['artist'] if item['type'] == 'album' else item['album']}[/])"

        page_items.append((item, text))

    pick = Paginator(page_items).render()
    print(pick)
