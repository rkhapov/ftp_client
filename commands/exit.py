from infra.command import Command
from infra.environment import Environment
from protocol.ftp import FtpClient


class ExitCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        self.environment.closed = True
        print(client.execute('quit').text)

    @staticmethod
    def help():
        return 'exit from ftpie'

    @staticmethod
    def name():
        return 'exit'

    @staticmethod
    def format():
        return 'exit'
