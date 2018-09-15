from infra.command import Command
from infra.environment import Environment, ConnectionMode
from protocol import address_parser
from protocol.ftp import FtpClient


class PortCommand(Command):
    def __init__(self, environment: Environment):
        super().__init__(environment)

    def execute(self, client: FtpClient):
        address = self.get_argument('address')
        if address_parser.parse_address_from_string(address) is None:
            raise ValueError('bad address format')

        self.environment.connection_mode = ConnectionMode.PORT
        self.environment.port_address = address

    @staticmethod
    def help():
        return 'use port connection mode for data transferring'

    @staticmethod
    def name():
        return 'port'

    @staticmethod
    def format():
        return 'port address'
