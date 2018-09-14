#!/usr/bin/env python3
from commands.command import Command
from commands.command import CommandParser
from network.client import FtpClient, FtpRequest, Actions


class List(Command):
    def execute(self, client: FtpClient):
        request = FtpRequest("LIST {}".format(' '.join(self.args[1:])))

    @property
    def name(self):
        return 'ls'

    @property
    def help(self):
        return 'print current folder content, possible keys are -l -a'


class ListParser(CommandParser):
    def parse(self, tokens):
        cmd = List()
        for i in range(1, len(tokens)):
            cmd.args.append(tokens[i])

        return cmd

    @property
    def parse_identifier(self):
        return 'list'

    @property
    def minimal_tokens_amount(self):
        return 1
