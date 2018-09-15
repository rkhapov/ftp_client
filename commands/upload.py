from infra.command import Command
from infra.environment import Environment
from protocol.ftp import FtpClient


class UploadCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        raise NotImplementedError

    @staticmethod
    def help():
        return 'upload filename as outfilename, if there is no outfilename, filename are used'

    @staticmethod
    def name():
        return 'upload'

    @staticmethod
    def format():
        return 'upload filename $outfilename'
