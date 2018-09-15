from infra.command import Command
from protocol.ftp import FtpClient


class HelpCommand(Command):
    def __init__(self, environment):
        super().__init__(environment)
        self.__commands = environment.commands

    def execute(self, client: FtpClient):
        if self.has_argument('command'):
            self._print_command_info()
            return

        print('ftpie - simple ftp client')
        print('list of available commands:')
        for cmd in self.__commands:
            print(cmd.name())
        print('see help <command> for command details')

    @staticmethod
    def help():
        return 'print help for all commands or for one command'

    @staticmethod
    def name():
        return 'help'

    @staticmethod
    def format():
        return 'help $command'

    def _print_command_info(self):
        name = self.get_argument('command')

        for cmd in self.__commands:
            if cmd.name() == name:
                print(cmd.format())
                print(cmd.help())
                return

        print('unknown command: {}'.format(name))
