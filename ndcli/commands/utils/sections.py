# Copyright (c) 2024 iiPython

# Modules
from typing import List, Tuple

from term_image.image import from_url

from ndcli.api import subsonic
from .show import bytes_to_human, duration, rlen

# Typing
Field = Tuple[str, str]
Section = Tuple[str, List[Field]]

# Handle section formatting and construction
def construct_sections(sections: List[Section]) -> List[str]:
    formatted_sections = []
    for name, fields in sections:
        lines = [f"[white on black] {name} [/]"]
        for name, value in fields:
            if value is None:
                continue

            lines.append(f"[yellow]{name}{':' if value else ''}[/] {value}" if value != "\x00" else name)

        length = rlen(max(lines, key = lambda x: rlen(x)))
        formatted_sections.append([line + (" " * (length - rlen(line))) for line in lines])

    longest_section = len(max(formatted_sections, key = lambda x: len(x)))

    print_text = [""] * longest_section
    for section in formatted_sections:
        section += [" " * rlen(section[0])] * (longest_section - len(section))
        for index, item in enumerate(section):
            print_text[index] += item + " " * 5

    return print_text

# Handle "building" sections
def truncate(items: List[Field], amount: int) -> List[Field]:
    if len(items) > amount:
        items = items[:amount] + [(f"[/][bright_black].. and {len(items) - amount} more ..[/][yellow]", "")]

    return items

def build_artist(artist: dict, albums: List[dict], top_songs: List[dict]) -> List[Section]:
    return [
        ("General", [
            ("Play Count", artist["playCount"]),
            ("Album Count", artist["albumCount"]),
            ("Song Count", artist["songCount"]),
            ("Size", bytes_to_human(artist["size"]))
        ]),
        ("Albums", truncate([
            (f"{album['name']} [bright_black]({album['year']})[/]", "")
            for album in sorted(
                [item | {"year": item.get("originalDate", item["date"]).split("-")[0]} for item in albums],
                key = lambda x: x["year"],
                reverse = True
            )
        ], 5)),
        ("Top Songs", [
            (f"{song['title']} [bright_black]({song['album']})[/]", "")
            for song in top_songs[:5]
        ]),
        ("Genres", [(genre["name"], "") for genre in artist.get("genres", [{"name": "None."}])])
    ]

def build_album(album: dict, tracks: List[dict]) -> List[Section]:
    return [
        ("General", [
            ("Play Count", album["playCount"]),
            ("Release Date", album.get("releaseDate")),
            ("Original Date", album.get("originalDate") if album.get("releaseDate") != album.get("originalDate") else None),
            ("Genre", album.get("genre") or "unknown"),
            ("Discs", len(album.get("discs", [0]))),
            ("Song Count", album["songCount"]),
            ("Length", f"{duration(album['duration'])}"),
            ("Size", bytes_to_human(album["size"])),
        ]),
        ("Tracks", truncate([
            (f"{track['title']} [bright_black]({duration(track['duration'])})[/]", "")
            for track in sorted(tracks, key = lambda x: x["trackNumber"])
        ], 7)),
        ("Cover Art", [
            (f"\x00{line}", "\x00")
            for line in str(from_url(
                subsonic.build_request("get", "getCoverArt.view", params = {"id": album["id"], "size": 10}).url,
                height = 10
            )).split("\n")
        ])
    ]

def build_song(song: dict) -> List[Section]:
    return [
        ("General", [
            ("Album", song["album"]),
            ("Play Count", song["playCount"]),
            ("Track Number", song["track"]),
            ("Release Year", song["year"]),
            ("Genre", song.get("genre") or "unknown")
        ]),
        ("File", [
            ("Bitrate", f"{song['bitRate']}kbps"),
            ("BPM", f"{song['bpm'] if song.get('bpm') else 'unknown'}"),
            ("Channels", song["channelCount"]),
            ("Sample Rate", f"{song['samplingRate'] / 1000}kHz"),
            ("File Type", song["contentType"]),
            ("Length", f"{duration(song['duration'])}"),
            ("Size", bytes_to_human(song["size"]))
        ])
    ]
