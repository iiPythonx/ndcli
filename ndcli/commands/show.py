# Copyright (c) 2024 iiPython

# Modules
import click

from . import ndcli

from ndcli import console
from ndcli.api import subsonic, navidrome
from ndcli.utils.paging import Paginator

from .utils.sections import construct_sections, build_artist, build_album, build_song

# Handle showing items
def show_item(item: dict) -> None:
    header_string = f"[white on black] {item['type'].upper()} [/] [blue]{item['title' if item['type'] == 'song' else 'name']}[/]"
    if item["type"] != "artist":
        header_string += f" by [blue]{item['artist']}[/]"

    if "userRating" in item:
        header_string += f" [bright_black]{'★' * item['userRating']}"

    console.print(header_string, highlight = False)

    # Handle sections
    match item["type"]:
        case "artist":
            with console.status("[blue]Loading artist info...", spinner = "arc"):
                sections = build_artist(
                    navidrome.get_artist(item["id"]),
                    navidrome.get_albums(order = "DESC", sort = "releaseDate", artist_id = item["id"]),
                    subsonic.get_top_songs(artist = item["name"])
                )

        case "album":
            with console.status("[blue]Loading album info...", spinner = "arc"):
                sections = build_album(
                    navidrome.get_album(item["id"]),
                    navidrome.get_tracks(album_id = item["id"])
                )

        case "song":
            sections = build_song(item)

    console.print("\n" + "\n".join(construct_sections(sections)) + "\n", highlight = False)

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
        return show_item(direct_matches[0])

    # Handle selection
    page_items = []
    for item in results:
        text = f"{item['title' if item['type'] == 'song' else 'name']} [bright_black]({item['type'].capitalize()})"
        if item["type"] in ["song", "album"]:
            text = text[:-1] + f", [yellow]{item['artist'] if item['type'] == 'album' else item['album']}[/])"

        page_items.append((item, text))

    show_item(Paginator(page_items).render())
