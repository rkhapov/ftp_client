from getpass import getpass

from infra.command import Command
from infra.environment import Environment
from protocol.ftp import FtpClient
from protocol.status import StatusCode


def _get_user():
    return input("User: ")


def _get_password():
    return getpass("Password: ")


class LoginCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        username = self.get_argument('user') if self.has_argument('user') else _get_user()
        password = self.get_argument('password') if self.has_argument('password') else _get_password()

        user_reply = client.execute('user {}'.format(username))

        if user_reply.status_code != StatusCode.USER_OKAY_NEED_PASSWORD.value:
            print(user_reply.text)
            return

        password_reply = client.execute('pass {}'.format(password))

        print(password_reply.text)

    @staticmethod
    def help():
        return 'login to system, supports logging without password echo'

    @staticmethod
    def name():
        return 'login'

    @staticmethod
    def format():
        return 'login $user $password'
