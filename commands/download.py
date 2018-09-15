from infra.command import Command
from infra.environment import Environment
from protocol.ftp import FtpClient


class DownloadCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        raise NotImplemented

    @staticmethod
    def help():
        return 'download file <filename> to <outfilename>, if there is not <outfilename>, <filename> are used'

    @staticmethod
    def name():
        return 'download'

    @staticmethod
    def format():
        return 'download filename $outfilename'
