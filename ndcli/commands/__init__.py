# Copyright (c) 2024 iiPython

# Modules
import click
from typing import Callable

from .. import console

# Initialization
def erase_last_line(text: str | None = None, lines: int = 1) -> None:
    print(f"\033[{lines}F\033[2K", end = "")  # This is fun.
    if text is not None:
        console.print(text)

# Handle group
class DefaultCommandGroup(click.Group):
    def command(self, *args, **kwargs) -> Callable:
        default_command = kwargs.pop("default_command", False)
        if default_command and not args:
            kwargs["name"] = kwargs.get("name", "<>")

        decorator = super(DefaultCommandGroup, self).command(*args, **kwargs)
        if default_command:
            def new_decorator(func: Callable) -> Callable:
                cmd = decorator(func)
                self.default_command = cmd.name
                return cmd

            return new_decorator

        return decorator

    def resolve_command(self, ctx, args) -> tuple:
        try:
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)

        except click.UsageError:
            args.insert(0, self.default_command)
            return super(DefaultCommandGroup, self).resolve_command(ctx, args)

@click.group(cls = DefaultCommandGroup, epilog = "Copyright (c) 2024 iiPython")
def ndcli() -> None:
    """A CLI for interacting with the Navidrome/Subsonic API.
    
    \b
    Source code: https://github.com/iiPythonx/ndcli
    """
    return
