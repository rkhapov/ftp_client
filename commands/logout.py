from infra.command import Command
from infra.environment import Environment
from protocol.ftp import FtpClient


class LogoutCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        pass

    @staticmethod
    def help():
        return 'logout current user'

    @staticmethod
    def name():
        return 'logout'

    @staticmethod
    def format():
        return 'logout'
