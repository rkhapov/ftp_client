#!/usr/bin/env python3
import re

from infra.command import Command, CommandParser


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
