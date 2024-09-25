# Copyright (c) 2024 iiPython

# Modules
import re
from datetime import timedelta

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

# Handle duration strings
def duration(duration: int | float) -> str:
    formatted = str(timedelta(seconds = duration))
    return formatted.split(".")[0]  # Remove microseconds
