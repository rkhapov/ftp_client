import re

from commands import *
from infra.command import Command
from infra.environment import Environment
from tools.splitter import split_without_escaped


def _create_command(cmd, tokens, environment):
    format_tokens = split_without_escaped(cmd.format())[1:]
    tokens = tokens[1:]

    if len(tokens) < len([f for f in format_tokens if not f.startswith('$')]):
        raise ValueError('no enough arguments')

    instance = cmd(environment)

    for arg in zip(format_tokens, tokens):
        key = arg[0] if not arg[0].startswith('$') else arg[0][1:]
        value = arg[1]

        instance.add_argument(key, value)

    return instance


class CommandFactory:
    def __init__(self):
        self.__commands = Command.__subclasses__()

    @property
    def commands(self):
        return self.__commands

    def from_string(self, cmd: str, environment: Environment):
        tokens = [f.replace(r'\ ', ' ') for f in split_without_escaped(cmd)]

        if len(tokens) == 0:
            raise ValueError('empty string')

        for cmd in self.__commands:
            if cmd.name().lower() == tokens[0].lower():
                return _create_command(cmd, tokens, environment)

        raise ValueError('unknown command')
