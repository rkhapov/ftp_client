from infra.command import Command
from infra.environment import Environment, ConnectionMode
from protocol.ftp import FtpClient


class PortCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        self.environment.connection_mode = ConnectionMode.PORT
        print('Entered port mode')

    @staticmethod
    def help():
        return 'use port connection mode for data transferring'

    @staticmethod
    def name():
        return 'port'

    @staticmethod
    def format():
        return 'port'
