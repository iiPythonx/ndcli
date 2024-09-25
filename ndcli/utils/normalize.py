# Copyright (c) 2024 iiPython

# Handle normalization
def track(track: dict) -> dict:
    return {
        "track": track["trackNumber"],
        "channelCount": track["channels"],
        "samplingRate": track["sampleRate"],
        "contentType": f"audio/{track['suffix']}",
        **track
    }
