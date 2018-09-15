from infra.command import Command
from infra.environment import Environment
from protocol.ftp import FtpClient


class CdCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        raise NotImplementedError

    @staticmethod
    def help():
        return 'change working directory (you can use .. for parent directory)'

    @staticmethod
    def name():
        return 'cd'

    @staticmethod
    def format():
        return 'cd directory'
