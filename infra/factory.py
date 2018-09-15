import re

from commands import *
from infra.command import Command
from infra.environment import Environment


def _create_command(cmd, tokens, environment):
    format_tokens = [f.lower() for f in re.split('[ \t]', cmd.format()) if f != ''][1:]
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
        tokens = [s.lower() for s in re.split('[ \t]', cmd) if s != '']

        if len(tokens) == 0:
            raise ValueError('empty string')

        for cmd in self.__commands:
            if cmd.name() == tokens[0]:
                return _create_command(cmd, tokens, environment)

        raise ValueError('unknown command')
