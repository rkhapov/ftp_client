import os

from infra.command import Command
from protocol.ftp import FtpClient


class ClearCommand(Command):
    def __init__(self, environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def help():
        return 'clears screen'

    @staticmethod
    def name():
        return 'clear'

    @staticmethod
    def format():
        return 'clear'
