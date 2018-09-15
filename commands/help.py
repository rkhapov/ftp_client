from infra.command import Command
from infra.environment import Environment
from protocol.ftp import FtpClient


class HelpCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        raise NotImplemented

    @staticmethod
    def help():
        return 'print help for all commands ot for one command'

    @staticmethod
    def name():
        return 'help'

    @staticmethod
    def format():
        return 'help $command'
