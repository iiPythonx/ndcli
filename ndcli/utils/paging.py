# Copyright (c) 2024 iiPython

# Modules
import atexit
from typing import Tuple
from readchar import readkey, key

from .. import console

# Pagination class
class Paginator():
    def __init__(self, options: Tuple[str, str], page_size: int = 10) -> None:
        self.pages = [options[i * page_size:(i + 1) * page_size] for i in range((len(options) + page_size - 1) // page_size )] 
        atexit.register(self.cleanup)

    def cleanup(self) -> None:
        print("\033[H\033[2J\033[?25h", end = "")

    def render(self) -> None:
        print("\033[2J\033[?25l", end = "")
        page, index = 0, 0
        while True:
            if index + 1 > len(self.pages[page]):
                index = 0

            print("\033[H", end = "")
            for item, (_, text) in enumerate(self.pages[page]):
                console.print(f"\033[2K{'[blue]' if index == item else ''} > {text}", highlight = False)

            print(f"\n <  Page {page + 1}/{len(self.pages)}  >")

            # Handle keypresses
            press = readkey()
            if press == key.UP and index:
                index -= 1

            elif press == key.DOWN and index + 1 < len(self.pages[page]):
                index += 1

            elif press == key.LEFT and page:
                page -= 1
                print("\033[1J")

            elif press == key.RIGHT and page + 1 < len(self.pages):
                page += 1
                print("\033[1J")

            elif press == key.ENTER:
                for item, (value, _) in enumerate(self.pages[page]):
                    if item == index:
                        atexit.unregister(self.cleanup)
                        self.cleanup()
                        return value
