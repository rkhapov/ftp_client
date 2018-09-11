#!/usr/bin/env python3

import os
import sys
from abc import abstractmethod
from enum import Enum
from getpass import getpass, getuser

from tools.sizeparser import extract_size_from_text
from client import downloader
from client.ftpconnection import FtpConnection
from client.resultstatusparser import ResultStatusParser
from client.tcpconnection import TcpConnection
from tools.addressparser import AddressParser
from client.uploader import upload_at_connection, upload_file_at_connection


class CommandStatus(Enum):
    SUCCESS = 1
    FAILED = 2


def _enter_passive_mode(connection: FtpConnection):
    connection.send("PASV")
    answer = connection.receive()
    print(answer)
    addr = AddressParser.extract_address_from_text(answer)

    if addr is None:
        return None

    return AddressParser.parse(addr)


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
        address = _enter_passive_mode(connection)
        if address is None:
            return CommandStatus.FAILED
        download_connection = TcpConnection(address[0], address[1])
        connection.send("LIST")
        print(connection.receive())
        decode = downloader.download_data_from_connection(download_connection).decode('utf-8')
        print(decode)

        return CommandStatus.SUCCESS

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
        answer = connection.receive()
        print(answer)
        code = ResultStatusParser.get_status_code(answer)
        if not ResultStatusParser.is_success_code(code):
            return CommandStatus.FAILED

        return CommandStatus.SUCCESS

    @staticmethod
    def name():
        return 'cd'

    @staticmethod
    def format():
        return 'cd $1'

    @staticmethod
    def help():
        return 'change current directory to specified (.. for parent directory)'


class PwdCommand(Command):
    def execute(self, connection: FtpConnection) -> CommandStatus:
        connection.send('PWD')
        answer = connection.receive()
        print(answer)
        code = ResultStatusParser.get_status_code(answer)
        if not ResultStatusParser.is_success_code(code):
            return CommandStatus.FAILED

        return CommandStatus.SUCCESS

    @staticmethod
    def name() -> str:
        return 'pwd'

    @staticmethod
    def format() -> str:
        return 'pwd'

    @staticmethod
    def help() -> str:
        return 'show current directory'


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
        address = _enter_passive_mode(connection)
        if address is None:
            return CommandStatus.FAILED
        upload_connection = TcpConnection(address[0], address[1])
        connection.send("STOR {}".format(self.args[0]))
        upload_file_at_connection(upload_connection, self.args[0])
        answer = connection.receive()
        code = ResultStatusParser.get_status_code(answer)

        if not ResultStatusParser.is_ok_code(code):
            return CommandStatus.FAILED

        return CommandStatus.SUCCESS

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
        address = _enter_passive_mode(connection)
        if address is None:
            return CommandStatus.FAILED
        download_connection = TcpConnection(address[0], address[1])
        connection.send("RETR {}".format(self.args[0]))
        answer = connection.receive_next_line()
        print(answer)
        code = ResultStatusParser.get_status_code(answer)
        if not ResultStatusParser.is_ok_code(code):
            return CommandStatus.FAILED
        size = extract_size_from_text(answer)
        downloader.download_file_from_connection(download_connection, self.args[1], size)
        answer = connection.receive()
        print(answer)
        code = ResultStatusParser.get_status_code(answer)
        if not ResultStatusParser.is_ok_code(code):
            return CommandStatus.FAILED

        return CommandStatus.SUCCESS

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


class RemoveFile(Command):
    def execute(self, connection: FtpConnection):
        connection.send('DELE {}'.format(self.args[0]))
        answer = connection.receive()
        print(answer)

        code = ResultStatusParser.get_status_code(answer)

        if not ResultStatusParser.is_success_code(code):
            return CommandStatus.FAILED

        return CommandStatus.SUCCESS

    @staticmethod
    def name():
        return 'rmf'

    @staticmethod
    def format():
        return 'rmf $1'

    @staticmethod
    def help():
        return 'remove file'


class RemoveDir(Command):
    def execute(self, connection: FtpConnection):
        connection.send('RMD {}'.format(self.args[0]))
        answer = connection.receive()
        print(answer)

        code = ResultStatusParser.get_status_code(answer)

        if not ResultStatusParser.is_success_code(code):
            return CommandStatus.FAILED

        return CommandStatus.SUCCESS

    @staticmethod
    def name():
        return 'rmd'

    @staticmethod
    def format():
        return 'rmd $1'

    @staticmethod
    def help():
        return 'remove directory'


class MakeDirectory(Command):
    def execute(self, connection: FtpConnection):
        connection.send("MKD {}".format(self.args[0]))
        answer = connection.receive()
        print(answer)

        code = ResultStatusParser.get_status_code(answer)

        if not ResultStatusParser.is_success_code(code):
            return CommandStatus.FAILED

        return CommandStatus.SUCCESS

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
        user, password = self._get_user_and_password()
        connection.send('USER {}'.format(user))
        answer = connection.receive()
        print(answer)
        result_code = ResultStatusParser.get_status_code(answer)

        if not ResultStatusParser.is_success_code(result_code) and \
                not ResultStatusParser.is_need_more_command_code(result_code):
            return CommandStatus.FAILED

        connection.send('PASS {}'.format(password))
        answer = connection.receive()
        print(answer)
        result_code = ResultStatusParser.get_status_code(answer)

        if not ResultStatusParser.is_success_code(result_code):
            return CommandStatus.FAILED

        return CommandStatus.SUCCESS

    def _get_user_and_password(self):
        user = input('User: ')
        password = getpass()

        return user, password


    @staticmethod
    def name() -> str:
        return 'login'

    @staticmethod
    def format() -> str:
        return 'login'

    @staticmethod
    def help() -> str:
        return 'login to system'
