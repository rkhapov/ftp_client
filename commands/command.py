#!/usr/bin/env python3

import sys
import os

from abc import abstractmethod
from enum import Enum

from client.ftpconnection import FtpConnection
from client.resultstatusparser import ResultStatusParser


class CommandStatus(Enum):
    SUCCESS = 1
    FAILED = 2


class Command:
    def __init__(self):
        self.args = []

    @abstractmethod
    def execute(self, connection: FtpConnection) -> CommandStatus:
        raise NotImplementedError('execute of command {} not implemented'.format(self.__class__.__name__))

    @staticmethod
    @abstractmethod
    def name() -> str:
        raise NotImplementedError('name method not implemented')

    @staticmethod
    @abstractmethod
    def format() -> str:
        raise NotImplementedError('format method not implemented')

    @staticmethod
    @abstractmethod
    def help() -> str:
        raise NotImplementedError('help method not implemented')


class List(Command):
    def execute(self, connection: FtpConnection):
        return CommandStatus.FAILED

    @staticmethod
    def name():
        return 'ls'

    @staticmethod
    def format():
        return 'ls'

    @staticmethod
    def help():
        return 'list of current directory files and subdirectories'


class ChangeDirectory(Command):
    def execute(self, connection: FtpConnection):
        connection.send('CWD {}'.format(self.args[0]))
        print(connection.receive())
        return CommandStatus.FAILED

    @staticmethod
    def name():
        return 'cd'

    @staticmethod
    def format():
        return 'cd $1'

    @staticmethod
    def help():
        return 'change directory to specified (.. for parent directory)'


class Quit(Command):
    def execute(self, connection: FtpConnection):
        connection.send('QUIT')
        connection.close()
        sys.exit(0)

    @staticmethod
    def name():
        return 'quit'

    @staticmethod
    def format():
        return 'quit'

    @staticmethod
    def help():
        return 'end session'


class Upload(Command):
    def execute(self, connection: FtpConnection):
        return CommandStatus.FAILED

    @staticmethod
    def name():
        return 'upload'

    @staticmethod
    def format():
        return 'upload $1'

    @staticmethod
    def help():
        return 'upload file or directory $1 to current directory'


class Download(Command):
    def execute(self, connection: FtpConnection):
        return CommandStatus.FAILED

    @staticmethod
    def name():
        return 'download'

    @staticmethod
    def format():
        return 'download $1 $2'

    @staticmethod
    def help():
        return 'download file or directory $1 from current directory to $2'


class Rename(Command):
    def execute(self, connection: FtpConnection):
        return CommandStatus.FAILED

    @staticmethod
    def name():
        return 'rename'

    @staticmethod
    def format():
        return 'rename $1 $2'

    @staticmethod
    def help():
        return 'rename file or directory $1 to $2'


class Remove(Command):
    def execute(self, connection: FtpConnection):
        return CommandStatus.FAILED

    @staticmethod
    def name():
        return 'remove'

    @staticmethod
    def format():
        return 'remove $1'

    @staticmethod
    def help():
        return 'remove file or directory'


class MakeDirectory(Command):
    def execute(self, connection: FtpConnection):
        return CommandStatus.FAILED

    @staticmethod
    def name():
        return 'mkdir'

    @staticmethod
    def format():
        return 'mkdir $1'

    @staticmethod
    def help():
        return 'make directory'


class Help(Command):
    def execute(self, connection: FtpConnection):
        print('Simple ftp client')
        print('Next commands are supported:')
        for command in Command.__subclasses__():
            print('{} : {}'.format(command.name() + ' ' * (15 - len(command.name())),
                                   command.help()))
        return CommandStatus.SUCCESS

    @staticmethod
    def name():
        return 'help'

    @staticmethod
    def format():
        return 'help'

    @staticmethod
    def help():
        return 'show help'


class CommandHelp(Command):
    def execute(self, connection: FtpConnection):
        for command in Command.__subclasses__():
            if command.name().lower() == self.args[0]:
                print('{}: [{}]: {}'.format(command.name(), command.format(), command.help()))
                return CommandStatus.SUCCESS

        print('Unknown command: {}'.format(self.args[0]))
        return CommandStatus.FAILED

    @staticmethod
    def name() -> str:
        return 'chelp'

    @staticmethod
    def format() -> str:
        return 'chelp $1'

    @staticmethod
    def help() -> str:
        return 'help for command $1'


class Clear(Command):
    def execute(self, connection: FtpConnection):
        os.system('cls' if os.name == 'nt' else 'clear')
        return CommandStatus.SUCCESS

    @staticmethod
    def name():
        return 'clear'

    @staticmethod
    def format():
        return 'clear'

    @staticmethod
    def help():
        return 'clear screen'


class Login(Command):
    def execute(self, connection: FtpConnection):
        connection.send('USER {}'.format(self.args[0]))
        result_code = ResultStatusParser.get_status_code(connection.receive())

        if not ResultStatusParser.is_success_code(result_code) and \
                not ResultStatusParser.is_need_more_command_code(result_code):
            return CommandStatus.FAILED

        connection.send('PASS {}'.format(self.args[1]))
        result_code = ResultStatusParser.get_status_code(connection.receive())

        if not ResultStatusParser.is_success_code(result_code):
            return CommandStatus.FAILED

        return CommandStatus.SUCCESS

    @staticmethod
    def name() -> str:
        return 'login'

    @staticmethod
    def format() -> str:
        return 'login $1 $2'

    @staticmethod
    def help() -> str:
        return 'login with user $1 and pass $2'
