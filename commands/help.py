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

        self.environment.writer.write('ftpie - simple ftp client')
        self.environment.writer.write('list of available commands:')
        for cmd in self.__commands:
            self.environment.writer.write(cmd.name())
        self.environment.writer.write('see help <command> for command details')

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
                self.environment.writer.write(cmd.format())
                self.environment.writer.write(cmd.help())
                return

        self.environment.writer.write('unknown command: {}'.format(name))
