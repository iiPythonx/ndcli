# Copyright (c) 2024 iiPython

# Modules
from typing import List, Tuple

from term_image.image import from_url

from ndcli.api import navidrome
from ndcli.api.typing import Artist, Album, Track
from .show import bytes_to_human, duration, rlen

# Typing
Field = Tuple[str, str | None]
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

def build_artist(artist: Artist, albums: List[dict], top_songs: List[dict]) -> List[Section]:
    sections = [
        ("General", [
            ("Play Count", artist.play_count),
            ("Album Count", artist.album_count),
            ("Song Count", artist.song_count),
            ("Size", bytes_to_human(artist.size))
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
        ])
    ]
    if artist.genres:
        sections.append(("Genres", [(genre, "") for genre in artist.genres]))

    return sections

def build_album(album: Album, tracks: List[dict]) -> List[Section]:
    return [
        ("General", [
            ("Play Count", album.play_count),
            ("Release Date", album.release_date),
            ("Original Date", album.original_date if album.release_date != album.original_date else None),
            ("Genre", album.genre or "unknown"),
            ("Discs", len(album.discs)),
            ("Song Count", album.song_count),
            ("Length", f"{duration(album.duration)}"),
            ("Size", bytes_to_human(album.size)),
        ]),
        ("Tracks", truncate([
            (f"{track['title']} [bright_black]({duration(track['duration'])})[/]", "")
            for track in sorted(tracks, key = lambda x: x["trackNumber"])
        ], 7)),
        ("Cover Art", [
            (f"\x00{line}", "\x00")
            for line in str(from_url(
                navidrome.build_subsonic("get", "getCoverArt.view", params = {"id": album.id, "size": 10}).url,
                height = 10,
                width = 23
            )).split("\n")
        ])
    ]

def build_track(track: Track) -> List[Section]:
    return [
        ("General", [
            ("Album", track.album),
            ("Play Count", track.play_count),
            ("Track Number", track.track),
            ("Release Year", track.year),
            ("Genre", ", ".join(track.genres))
        ]),
        ("File", [
            ("Bitrate", f"{track.bitrate}kbps"),
            ("BPM", track.bpm or "unknown"),
            ("Channels", track.channels),
            ("Sample Rate", f"{track.sample_rate / 1000}kHz"),
            ("File Type", track.mimetype),
            ("Length", f"{duration(track.duration)}"),
            ("Size", bytes_to_human(track.size))
        ])
    ]
