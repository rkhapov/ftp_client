#!/usr/bin/env python3
import os

from commands.command import Command
from importlib import import_module


def _get_submodules():
    parts = __name__.split('.')
    result = ''

    for i in range(len(parts) - 1):
        result += parts[i] + '.'

    return result


files = [os.path.splitext(f)[0] for f in os.listdir(os.path.dirname(__file__)) if
         not f.startswith('__') and f != os.path.basename(__file__) and f.endswith(".py")]

for f in files:
    import_module('{}{}'.format(_get_submodules(), f))


class CommandFactory:
    def __init__(self):
        self.__commands = Command.__subclasses__()

    @property
    def commands(self):
        return self.__commands

    def from_string(self, command: str):
        print(self.__commands)


if __name__ == "__main__":
    print(CommandFactory().commands)
