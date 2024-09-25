# Copyright (c) 2024 iiPython

class Mapping:
    ARTIST = {
        "playCount": "play_count",
        "playDate": "play_date",
        "rating": "rating",
        "starred": "starred",
        "starredAt": "starred_at",
        "id": "id",
        "name": "name",
        "albumCount": "album_count",
        "songCount": "song_count",
        "genres": ("genres", lambda x: [genre["name"] for genre in x or []]),
        "size": "size"
    }
    ALBUM = {
        "playCount": "play_count",
        "playDate": "play_date",
        "rating": "rating",
        "starredAt": "starred_at",
        "id": "id",
        "name": "name",
        "artist": "artist",
        "albumArtist": "album_artist",
        "date": "date",
        "originalDate": "original_date",
        "releaseDate": "release_date",
        "songCount": "song_count",
        "duration": "duration",
        "size": "size",
        "genre": "genre",
        "discs": "discs" 
    }
    TRACK = {
        "playCount": "play_count",
        "played": "play_date",
        "id": "id",
        "title": "name",
        "artist": "artist",
        "album": "album",
        "track": "track",
        "year": "year",
        "contentType": "mimetype",
        "bpm": ("bpm", lambda x: None if not x else x),
        "bitRate": "bitrate",
        "duration": "duration",
        "size": "size",
        "genres": ("genres", lambda x: [genre["name"] for genre in x]),
        "channelCount": "channels",
        "samplingRate": "sample_rate"
    }

class TypedObject():
    def __init__(self, payload: dict, mapping: dict) -> None:
        for k, v in payload.items():
            if k not in mapping:
                continue

            replacement = mapping[k]
            if isinstance(replacement, tuple):
                replacement, v = replacement[0], replacement[1](v)

            setattr(self, replacement, v)

class Artist(TypedObject):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload, Mapping.ARTIST)

class Album(TypedObject):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload, Mapping.ALBUM)

class Track(TypedObject):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload, Mapping.TRACK )
