#!/usr/bin/env python3
import re

from commands.command import Command


class CommandFactoryError(Exception):
    def __init_(self, msg: str):
        super().__init__(msg)


class CommandFactory:
    def __init__(self):
        self._commands = Command.__subclasses__()

    def from_string(self, command: str) -> Command:
        tokens = [s for s in re.split('[ \t]', command) if s != '']

        if len(tokens) < 1:
            raise CommandFactoryError('Expected non-empty string')

        for cmd in self._commands:
            if cmd.name().lower() == tokens[0].lower():
                return CommandFactory._parse_cmd(tokens, cmd)

        raise CommandFactoryError('Unknown command: {}'.format(tokens[0]))

    @staticmethod
    def _parse_cmd(tokens, cmd: type(Command)) -> Command:
        cmd_tokens = re.split('[ \t]', cmd.format())

        if len(cmd_tokens) != len(tokens):
            raise CommandFactoryError('Unexpected arguments number for command {}: {}'.format(cmd.name(), len(tokens)))

        command = cmd()

        for i in range(len(cmd_tokens)):
            if CommandFactory._is_argument(cmd_tokens[i]):
                command.args.append(tokens[i])
            elif tokens[i].lower() != cmd_tokens[i].lower():
                raise CommandFactoryError('Unknown part of command {}: {}'.format(cmd.name(), tokens[i]))

        return command

    @staticmethod
    def _is_argument(token: str) -> bool:
        return token.startswith('$') and len(token) > 1 and token[1:].isnumeric()

