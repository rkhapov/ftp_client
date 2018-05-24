#!/usr/bin/env python3


from abc import abstractmethod
from client.connection import Connection


class Command:
    @abstractmethod
    def execute(self, connection: Connection):
        raise NotImplementedError('execute of command {} not implemented'.format(self.__class__.__name__))

    @staticmethod
    @abstractmethod
    def name():
        raise NotImplementedError('name method not implemented')

    @staticmethod
    @abstractmethod
    def format():
        raise NotImplementedError('format method not implemented')

    @staticmethod
    @abstractmethod
    def help():
        raise NotImplementedError('help method not implemented')


class ChangeDirectory(Command):
    def execute(self, connection: Connection):
        print(self.__class__.__name__)

    @staticmethod
    def name():
        return 'cd'

    @staticmethod
    def format():
        return 'cd $1'

    @staticmethod
    def help():
        return 'Change directory to specified (.. for parent directory)'


class Quit(Command):
    def execute(self, connection: Connection):
        print(self.__class__.__name__)

    @staticmethod
    def name():
        return 'quit'

    @staticmethod
    def format():
        return 'quit'

    @staticmethod
    def help():
        return 'End session'


class Upload(Command):
    def execute(self, connection: Connection):
        print(self.__class__.__name__)

    @staticmethod
    def name():
        return 'upload'

    @staticmethod
    def format():
        return 'upload $1'

    @staticmethod
    def help():
        return 'Upload file or directory $1 to current directory'


class Download(Command):
    def execute(self, connection: Connection):
        print(self.__class__.__name__)

    @staticmethod
    def name():
        return 'download'

    @staticmethod
    def format():
        return 'download $1 $2'

    @staticmethod
    def help():
        return 'Download file or directory $1 from current directory to $2'


class Rename(Command):
    def execute(self, connection: Connection):
        print(self.__class__.__name__)

    @staticmethod
    def name():
        return 'rename'

    @staticmethod
    def format():
        return 'rename $1 $2'

    @staticmethod
    def help():
        return 'Rename file or directory $1 to $2'


class Remove(Command):
    def execute(self, connection: Connection):
        print(self.__class__.__name__)

    @staticmethod
    def name():
        return 'remove'

    @staticmethod
    def format():
        return 'remove $1'

    @staticmethod
    def help():
        return 'Remove file or directory $1'


class MakeDirectory(Command):
    def execute(self, connection: Connection):
        print(self.__class__.__name__)

    @staticmethod
    def name():
        return 'mkdir'

    @staticmethod
    def format():
        return 'mkdir $1'

    @staticmethod
    def help():
        return 'Make directory'


class Help(Command):
    def execute(self, connection: Connection):
        for command in Command.__subclasses__():
            print('{} [{}]: {}'.format(command.name(), command.format(), command.help()))

    @staticmethod
    def name():
        return 'help'

    @staticmethod
    def format():
        return 'help'

    @staticmethod
    def help():
        return 'Show this help'
