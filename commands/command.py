#!/usr/bin/env python3


from abc import abstractmethod
from client.connection import Connection


class Command:
    @abstractmethod
    def execute(self, connection: Connection):
        raise NotImplementedError('execute of command {} not implemented'.format(self.__class__.__name__))


class ChangeDirectory(Command):
    pass


class Quit(Command):
    pass


class GoToParentDirectory(Command):
    pass


class UploadFile(Command):
    pass


class UploadDirectory(Command):
    pass


class DownloadFile(Command):
    pass


class DownloadDirectory(Command):
    pass


class RenameFile(Command):
    pass


class RemoveDirectory(Command):
    pass


class RemoveFile(Command):
    pass


class MakeDirectory(Command):
    pass
