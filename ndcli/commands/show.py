# Copyright (c) 2024 iiPython

# Modules
import click

from . import ndcli

from ndcli import console
from ndcli.api import navidrome
from ndcli.api.typing import Artist, Album, Track, TypedObject
from ndcli.utils.paging import Paginator

from .utils.sections import construct_sections, build_artist, build_album, build_track

# Handle showing items
def show_item(item: TypedObject) -> None:
    header_string = f"[white on black] {type(item).__name__.upper()} [/] [blue]{item.name}[/]"
    if not isinstance(item, Artist):
        header_string += f" by [blue]{item.artist}[/]"

    if hasattr(item, "rating"):
        header_string += f" [bright_black]{'★' * item.rating}"

    console.print(header_string, highlight = False)

    # Handle sections
    if isinstance(item, Artist):
        with console.status("[blue]Loading artist info...", spinner = "arc"):
            sections = build_artist(
                item,
                navidrome.get_albums(order = "DESC", sort = "releaseDate", artist_id = item.id),
                navidrome.get_top_songs(artist = item.name)
            )

    elif isinstance(item, Album):
        with console.status("[blue]Loading album info...", spinner = "arc"):
            sections = build_album(
                item,
                navidrome.get_tracks(album_id = item.id)
            )

    elif isinstance(item, Track):
        sections = build_track(item)

    print()
    for line in construct_sections(sections):
        with console.capture() as capture:
            console.print(line.split("\x00")[0], highlight = False, end = "")

        arguments = [capture.get()]
        if "\x00" in line:
            arguments.append(line.split("\x00")[1])

        print(*arguments, sep = "")

    print()

# Commands
@ndcli.command("show", default_command = True)
@click.argument("query", nargs = -1)
def show_command(query: str) -> None:
    """Search and show any Navidrome item."""

    # Normalize our query
    actual_query = " ".join(query).strip().lower()
    with console.status("[blue]Searching...", spinner = "arc"):
        response = navidrome.search(actual_query, 4, 4, 4)

    # Begin matching
    direct_matches = [item for item in response if item.name.lower() == actual_query]
    if len(direct_matches) == 1:
        return show_item(direct_matches[0])

    # Handle selection
    page_items = []
    for item in response:
        text = f"{item.name} [bright_black]({type(item).__name__})"
        if isinstance(item, (Album, Track)):
            text = text[:-1] + f", [yellow]{item.artist if isinstance(item, Album) else item.album}[/])"

        page_items.append((item, text))

    show_item(Paginator(page_items).render())
