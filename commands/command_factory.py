#!/usr/bin/env python3


from commands.command import Command


class CommandFactory:
    def __init__(self):
        self._commands = Command.__subclasses__()

    def from_string(self, command: str) -> Command:
        raise NotImplementedError
