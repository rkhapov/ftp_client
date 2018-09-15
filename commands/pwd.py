from infra.command import Command
from protocol.ftp import FtpClient


class PwdCommand(Command):
    def execute(self, client: FtpClient):
        raise NotImplemented

    @staticmethod
    def help():
        return 'print working directory'

    @staticmethod
    def name():
        return 'pwd'

    @staticmethod
    def format():
        return 'pwd'
