from infra.command import Command
from infra.environment import Environment, ConnectionMode
from protocol.ftp import FtpClient


class PasvCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        self.environment.connection_mode = ConnectionMode.PASSIVE
        self.environment.writer.write('Entered passive mode')

    @staticmethod
    def help():
        return 'enable passive mod for every download\\upload operations'

    @staticmethod
    def name():
        return 'pasv'

    @staticmethod
    def format():
        return 'pasv'
