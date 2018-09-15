from infra.command import Command
from infra.environment import Environment
from protocol.ftp import FtpClient


class ListCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        raise NotImplemented

    @staticmethod
    def help():
        return 'print directory content'

    @staticmethod
    def name():
        return 'ls'

    @staticmethod
    def format():
        return 'ls $dir'
