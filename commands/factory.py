#!/usr/bin/env python3
import os
import re

from commands.command import Command, CommandParser
from importlib import import_module

# crutch for import all files from directory
# what the fuck!
# why i must do this by myself???!!!


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
        self.__parsers = CommandParser.__subclasses__()

    @property
    def commands(self):
        return self.__commands

    @property
    def parsers(self):
        return self.__parsers

    def from_string(self, cmd: str):
        tokens = [s for s in re.split('[ \t]', cmd)]

        for parser in self.__parsers:
            if tokens[0].lower() == parser.parse_identifier:
                if len(tokens) < parser.minimal_tokens_amount:
                    raise ValueError('no enough tokens to parse {}'.format(parser.parse_identifier))

        raise NotImplemented('no parser found for {}'.format(tokens[0].lower()))
