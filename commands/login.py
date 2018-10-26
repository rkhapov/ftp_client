from getpass import getpass

from infra.command import Command
from infra.environment import Environment
from protocol.ftp import FtpClient
from protocol.status import StatusCode


def _get_user(env):
    return env.reader.read_next_command("User: ")


def _get_password(env):
    if env.reader.supports_hide:
        return env.reader.read_hide("Password: ")

    return env.reader.read_next_command("Password: ")


class LoginCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        username = self.get_argument('user') if self.has_argument('user') else _get_user(self.environment)
        password = self.get_argument('password') if self.has_argument('password') else _get_password(self.environment)

        user_reply = client.execute('user {}'.format(username))

        if user_reply.status_code != StatusCode.USER_OKAY_NEED_PASSWORD.value:
            self.environment.writer.write(user_reply.text)
            return

        password_reply = client.execute('pass {}'.format(password))

        self.environment.writer.write(password_reply.text)

    @staticmethod
    def help():
        return 'login to system, supports logging without password echo'

    @staticmethod
    def name():
        return 'login'

    @staticmethod
    def format():
        return 'login $user $password'
