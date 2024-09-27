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
        "discs": ("discs", lambda x: x or []),
        "year": "year"
    }
    TRACK = {
        "playCount": ("play_count", lambda x: x or 0),
        "played": "play_date",
        "id": "id",
        "title": "name",
        "artist": "artist",
        "album": "album",
        "track": "track",
        "year": "year",
        "trackNumber": "track",
        "discNumber": "disc",
        "contentType": "mimetype",
        "bpm": ("bpm", lambda x: None if not x else x),
        "bitRate": "bitrate",
        "duration": "duration",
        "size": "size",
        "genres": ("genres", lambda x: [genre["name"] for genre in (x or [])]),
        "channelCount": "channels",
        "samplingRate": "sample_rate"
    }

class TypedObject():
    def __init__(self, payload: dict, mapping: dict) -> None:
        for k, v in mapping.items():
            replacement, value = v, payload.get(k)
            if isinstance(v, tuple):
                replacement, value = v[0], v[1](value)

            setattr(self, replacement, value)

class Artist(TypedObject):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload, Mapping.ARTIST)

class Album(TypedObject):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload, Mapping.ALBUM)
        self.release_date = self.release_date or self.date
        self.original_date = self.original_date or self.date
        self.year = self.year or self.date.split("-")[0]

class Track(TypedObject):
    def __init__(self, payload: dict) -> None:
        super().__init__(payload, Mapping.TRACK)
