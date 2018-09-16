from infra.command import Command
from protocol.ftp import FtpClient


class PwdCommand(Command):
    def __init__(self, environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        print(client.execute('pwd').text)

    @staticmethod
    def help():
        return 'print working directory'

    @staticmethod
    def name():
        return 'pwd'

    @staticmethod
    def format():
        return 'pwd'
