from infra.command import Command
from infra.environment import Environment
from protocol.ftp import FtpClient


class LoginCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        raise NotImplementedError

    @staticmethod
    def help():
        return 'login to system, support logging without password echo'

    @staticmethod
    def name():
        return 'login'

    @staticmethod
    def format():
        return 'login $user $password'
