# Copyright (c) 2024 iiPython

# Modules
import re
from datetime import timedelta

import click

from . import ndcli

from ndcli import console
from ndcli.api import subsonic, navidrome
from ndcli.utils.paging import Paginator

# Handle checking length
def rlen(string: str) -> int:
    return len(re.sub(r"\[.*?]", "", string))

# Bytes conversion
# https://stackoverflow.com/a/31631711
def bytes_to_human(size: int) -> str:
    B = float(size)
    KB = float(1024)
    MB = float(KB ** 2)
    GB = float(KB ** 3)

    if KB <= B < MB:
        return "{0:.2f} KB".format(B / KB)

    elif MB <= B < GB:
        return "{0:.2f} MB".format(B / MB)

    elif GB <= B:
        return "{0:.2f} GB".format(B / GB)

# Handle showing items
def show_item(item: dict) -> None:
    print(item)
    header_string = f"[white on black] {item['type'].upper()} [/] [blue]{item['title' if item['type'] == 'song' else 'name']}[/]"
    if item["type"] != "artist":
        header_string += f" by [blue]{item['artist']}[/]"

    if "userRating" in item:
        header_string += f" [bright_black]{'★' * item['userRating']}"

    console.print(header_string, highlight = False)

    # Handle sections
    if item["type"] == "artist":
        with console.status("[blue]Loading artist info...", spinner = "arc"):
            artist = navidrome.get_artist(item["id"])
            releases = navidrome.get_albums(order = "DESC", sort = "releaseDate", artist_id = item["id"])
            top_songs = subsonic.get_top_songs(artist = item["name"])

        album_list = [
            (f"{album['name']} [bright_black]({album['year']})[/]", "")
            for album in sorted(
                [item | {"year": item.get("originalDate", item["date"]).split("-")[0]} for item in releases],
                key = lambda x: x["year"],
                reverse = True
            )
        ]
        if len(album_list) > 5:
            album_list = album_list[:5] + [(f"[/][bright_black].. and {len(album_list) - 6} more ..[/][yellow]", "")]

        sections = [
            ("General", [
                ("Play Count", artist["playCount"]),
                ("Album Count", artist["albumCount"]),
                ("Song Count", artist["songCount"]),
                ("Size", bytes_to_human(artist["size"]))
            ]),
            ("Albums", album_list)
        ]
        if "genres" in artist:
            sections.append(("Genres", [(genre["name"], "") for genre in artist["genres"]]))

        sections.append(("Top Songs", [
            (f"{song['title']} [bright_black]({song['album']})[/]", "")
            for song in top_songs[:5]
        ]))

    if item["type"] == "song":
        sections = [
            ("General", [
                ("Album", item["album"]),
                ("Play Count", item["playCount"]),
                ("Track Number", item["track"]),
                ("Release Year", item["year"]),
                ("Genre", item.get("genre", "unknown"))
            ]),
            ("File", [
                ("Bitrate", f"{item['bitRate']}kbps"),
                ("BPM", f"{item['bpm'] if item['bpm'] != 0 else 'unknown'}"),
                ("Channels", item["channelCount"]),
                ("Sample Rate", f"{item['samplingRate'] / 1000}kHz"),
                ("File Type", item["contentType"]),
                ("Length", f"{timedelta(seconds = item['duration'])}"),
                ("Size", bytes_to_human(item["size"]))
            ])
        ]

    formatted_sections = []
    for name, fields in sections:
        lines = [f"[white on black] {name} [/]"]
        for name, value in fields:
            lines.append(f"[yellow]{name}{':' if value else ''}[/] {value}")

        length = rlen(max(lines, key = lambda x: rlen(x)))
        formatted_sections.append([line + (" " * (length - rlen(line))) for line in lines])

    longest_section = len(max(formatted_sections, key = lambda x: len(x)))

    print_text = [""] * longest_section
    for section in formatted_sections:
        section += [" " * rlen(section[0])] * (longest_section - len(section))
        for index, item in enumerate(section):
            print_text[index] += item + " " * 5

    console.print("\n" + "\n".join(print_text) + "\n", highlight = False)

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
